import { AnalysisResponse } from "../types";

const API_BASE_URL = "http://localhost:8000";

export async function submitAnalysis(file: File, notes?: string): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  if (notes && notes.trim()) {
    formData.append("notes", notes.trim());
  }

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Analysis request failed.");
  }

  return response.json();
}