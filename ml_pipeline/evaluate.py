import torch
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from torchvision import models
import torch.nn as nn
from data_loader import get_data_loaders

def evaluate():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _, _, test_loader, class_to_idx = get_data_loaders(batch_size=32)
    idx_to_class = {v: k for k, v in class_to_idx.items()}

    model = models.resnet18()
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load("saved_models/pneumonia_resnet18.pth", map_location=device))
    model.to(device)
    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    target_names = [idx_to_class[i] for i in sorted(idx_to_class.keys())]

    print("\n--- Test Set Evaluation Report ---")
    print(classification_report(y_true, y_pred, target_names=target_names, digits=4))

    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(cm)
    print("\nNote: These metrics evaluate benchmark dataset performance and do not reflect standalone clinical diagnostic efficacy.")

if __name__ == "__main__":
    evaluate()