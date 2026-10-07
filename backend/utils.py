import io
import base64
from PIL import Image
import numpy as np
import cv2
import torch
from torchvision import transforms

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def get_inference_transform():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

def pil_to_base64(image: Image.Image, format="JPEG") -> str:
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{img_str}"

def overlay_heatmap_on_image(original_pil: Image.Image, heatmap_np: np.ndarray, alpha=0.4) -> Image.Image:
    original_resized = original_pil.convert("RGB").resize((224, 224))
    original_cv = np.array(original_resized)

    heatmap_uint8 = np.uint8(255 * heatmap_np)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

    blended = cv2.addWeighted(original_cv, 1 - alpha, heatmap_colored, alpha, 0)
    return Image.fromarray(blended)