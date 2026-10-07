import os
import torch
import torch.nn as nn
from torchvision import models
from torch.optim import Adam
from data_loader import get_data_loaders

def build_model(num_classes=2):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model

def train(epochs=10, batch_size=32, lr=1e-4):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    train_loader, val_loader, _, class_to_idx = get_data_loaders(batch_size=batch_size)
    print(f"Class mapping: {class_to_idx}")

    model = build_model().to(device)

    # Calculate class weights to handle dataset imbalance
    # Train set typically has ~3875 pneumonia vs ~1341 normal
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=lr, weight_decay=1e-4)

    best_val_loss = float("inf")
    os.makedirs("saved_models", exist_ok=True)
    save_path = "saved_models/pneumonia_resnet18.pth"

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        epoch_loss = running_loss / total
        epoch_acc = correct / total

        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_loss = val_loss / val_total if val_total > 0 else 0
        val_acc = val_correct / val_total if val_total > 0 else 0

        print(f"Epoch [{epoch+1}/{epochs}] | Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f} | Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), save_path)
            print(f"--> Saved best checkpoint to {save_path}")

    print("Training finished.")

if __name__ == "__main__":
    train()