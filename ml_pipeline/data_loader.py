import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

    return train_transform, val_test_transform

def get_data_loaders(base_dir="../dataset/chest_xray", batch_size=32):
    train_tf, val_test_tf = get_transforms()

    train_path = os.path.join(base_dir, "train")
    val_path = os.path.join(base_dir, "val")
    test_path = os.path.join(base_dir, "test")

    train_dataset = datasets.ImageFolder(train_path, transform=train_tf)
    val_dataset = datasets.ImageFolder(val_path, transform=val_test_tf)
    test_dataset = datasets.ImageFolder(test_path, transform=val_test_tf)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    return train_loader, val_loader, test_loader, train_dataset.class_to_idx