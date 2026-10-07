from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_routes import router

app = FastAPI(
    title="MedGuide AI API",
    description="AI-Assisted Clinical Second Opinion API for Chest X-Ray Analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "MedGuide"}