export interface AnalysisResponse {
  finding: "NORMAL" | "PNEUMONIA";
  confidence: number;
  original_image: string;
  heatmap: string;
  image_evidence: string;
  clinical_evidence?: string | null;
  assessment: string;
  openrouter_summary?: string | null;
  openrouter_status?: "not_configured" | "configured" | "success" | "error";
}