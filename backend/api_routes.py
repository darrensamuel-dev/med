import io
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
from inference import ModelEngine

router = APIRouter()
engine = ModelEngine()

@router.post("/predict")
async def predict_xray(
    file: UploadFile = File(...),
    notes: Optional[str] = Form(None)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a supported image.")

    try:
        image_bytes = await file.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    try:
        results = engine.predict(pil_image, patient_notes=notes)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return results