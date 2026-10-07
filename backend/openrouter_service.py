import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


class OpenRouterService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "nvidia/nemotron-3-ultra-550b-a55b:free",
        ).strip()
        self.base_url = os.getenv(
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1",
        ).rstrip("/")

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.api_key != "your_openrouter_api_key_here")

    def summarize(
        self,
        finding: str,
        confidence: float,
        image_evidence: str,
        clinical_evidence: str | None,
    ) -> str | None:
        if not self.configured:
            return None

        prompt = (
            "You are a clinical communication assistant for a research prototype. "
            "Summarize the provided model output without changing the classification, "
            "confidence, or evidence. Do not diagnose, invent findings, recommend treatment, "
            "or imply that the model is definitive. Mention that qualified clinical review "
            "is required. Return one concise paragraph.\n\n"
            f"Model classification: {finding}\n"
            f"Model confidence: {confidence:.4f}\n"
            f"Image evidence: {image_evidence}\n"
            f"Clinical notes evidence: {clinical_evidence or 'No clinical notes provided.'}"
        )
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Stay strictly grounded in the supplied fields.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0,
                "max_tokens": 180,
            }
        ).encode("utf-8")
        request = Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://127.0.0.1:3000",
                "X-Title": "MedGuide",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise ValueError("OpenRouter returned an empty summary.")
            return content.strip()
        except (HTTPError, URLError, KeyError, IndexError, TypeError, ValueError) as error:
            raise RuntimeError("OpenRouter summary request failed.") from error
