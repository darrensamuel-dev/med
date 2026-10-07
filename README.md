# MedGuide — AI-Assisted Clinical Second Opinion

MedGuide is a clinical second-opinion web platform that analyzes chest X-rays to detect pneumonia-associated radiographic patterns and highlights predictive regions using Grad-CAM.

## Architecture
- **ML Pipeline (`ml_pipeline/`)**: PyTorch ResNet18 fine-tuning, ImageNet preprocessing, evaluation metrics.
- **Backend API (`backend/`)**: FastAPI, Grad-CAM feature attribution engine, clinical notes grounding.
- **Frontend Dashboard (`frontend/`)**: React 18, Vite, TypeScript, Tailwind CSS, Lucide icons.

## Quick Start

### 1. Model Training
```bash
cd ml_pipeline
pip install -r requirements.txt
python train.py
python evaluate.py