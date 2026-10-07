import os
from pathlib import Path

import torch
import numpy as np
import torch.nn as nn
from torchvision import models
from PIL import Image
from utils import get_inference_transform, pil_to_base64, overlay_heatmap_on_image
from grad_cam import GradCAM
from openrouter_service import OpenRouterService

CLASS_NAMES = ["NORMAL", "PNEUMONIA"]
DEFAULT_WEIGHTS_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml_pipeline"
    / "saved_models"
    / "pneumonia_resnet18.pth"
)

class ModelEngine:
    def __init__(self, weights_path: str | os.PathLike[str] = DEFAULT_WEIGHTS_PATH):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet18()
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)
        self.weights_path = Path(weights_path)

        if self.weights_path.exists():
            self.model.load_state_dict(torch.load(self.weights_path, map_location=self.device))
            print(f"Loaded weights from {self.weights_path}")
        else:
            print(f"Warning: Weights not found at {self.weights_path}.")

        self.model.to(self.device)
        self.model.eval()
        self.transform = get_inference_transform()
        self.grad_cam = GradCAM(self.model, self.model.layer4[1].conv2)
        self.openrouter = OpenRouterService()

    def predict(self, image: Image.Image, patient_notes: str = None):
        if not self.weights_path.exists():
            raise RuntimeError(
                "The trained model weights are unavailable. Run ml_pipeline/train.py first."
            )

        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.set_grad_enabled(True):
            outputs = self.model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1).cpu().detach().numpy()[0]
            pred_idx = int(np.argmax(probabilities))
            confidence = float(probabilities[pred_idx])

            cam_map = self.grad_cam.generate(input_tensor, pred_idx)

        finding = CLASS_NAMES[pred_idx]
        original_resized = image.resize((224, 224))
        blended_image = overlay_heatmap_on_image(original_resized, cam_map)

        # Build grounded doctor-facing text
        conf_percent = round(confidence * 100)
        if finding == "PNEUMONIA":
            image_evidence = "The highlighted region indicates the area that contributed most to this prediction."
            assessment = (
                f"Doctor, consider this finding: the model detected features associated with pneumonia with "
                f"{conf_percent}% confidence. The highlighted region indicates the area that contributed most to this prediction."
            )
        else:
            image_evidence = "No localized focal densities strongly contributed toward a pneumonia prediction."
            assessment = (
                f"Doctor, consider this finding: the model classified this image as normal with "
                f"{conf_percent}% confidence based on standard thoracic features."
            )

        # Ground clinical evidence strictly in explicit notes
        clinical_evidence = None
        if patient_notes and patient_notes.strip():
            notes_lower = patient_notes.lower()
            detected_tokens = []
            known_cues = ["fever", "cough", "breath", "dyspnea", "crackles", "chest pain", "sputum", "tachypnea"]
            for cue in known_cues:
                if cue in notes_lower:
                    detected_tokens.append(cue)

            if detected_tokens:
                clinical_evidence = f"Patient notes explicitly state clinical indicators: {', '.join(detected_tokens)}."
            else:
                clinical_evidence = f"Patient notes provided: \"{patient_notes.strip()}\"."

        openrouter_summary = None
        openrouter_status = "not_configured"
        if self.openrouter.configured:
            openrouter_status = "configured"
            try:
                openrouter_summary = self.openrouter.summarize(
                    finding=finding,
                    confidence=confidence,
                    image_evidence=image_evidence,
                    clinical_evidence=clinical_evidence,
                )
                openrouter_status = "success"
            except RuntimeError:
                openrouter_status = "error"

        return {
            "finding": finding,
            "confidence": round(confidence, 4),
            "original_image": pil_to_base64(original_resized),
            "heatmap": pil_to_base64(blended_image),
            "image_evidence": image_evidence,
            "clinical_evidence": clinical_evidence,
            "assessment": assessment,
            "openrouter_summary": openrouter_summary,
            "openrouter_status": openrouter_status,
        }