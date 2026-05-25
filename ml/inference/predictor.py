from pathlib import Path
from uuid import uuid4

from backend.core.config import Settings, get_settings
from backend.models.domain import PredictionResult
from ml.explainability.grad_cam import build_grad_cam
from ml.knowledge_base import DISEASE_KNOWLEDGE
from ml.model_loader.plant_model import PlantDiseaseModel
from ml.preprocessing.image_preprocessor import ImagePreprocessor


class PlantDiseasePredictor:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.preprocessor = ImagePreprocessor()
        self.model = PlantDiseaseModel(self.settings)

    def predict(self, image_path: str | Path) -> PredictionResult:
        batch = self.preprocessor.preprocess(image_path)
        explanation_path = None
        if self.model.has_trained_model:
            label, confidence, _ = self.model.predict(batch)
            if self.model.model is not None:
                output = self.settings.upload_dir / f"gradcam_{uuid4().hex}.jpg"
                explanation_path = build_grad_cam(self.model.model, batch, image_path, output)
        else:
            label, confidence = self._heuristic_predict(image_path)
        knowledge = DISEASE_KNOWLEDGE.get(label, DISEASE_KNOWLEDGE["Generic___Healthy"])
        return PredictionResult(
            crop_name=str(knowledge["crop"]),
            disease_name=str(knowledge["disease"]),
            confidence=round(confidence, 4),
            symptoms=list(knowledge["symptoms"]),
            remedies=list(knowledge["remedies"]),
            fertilizer=list(knowledge["fertilizer"]),
            prevention=list(knowledge["prevention"]),
            explanation_path=explanation_path,
        )

    def _heuristic_predict(self, image_path: str | Path) -> tuple[str, float]:
        features = self.preprocessor.leaf_features(image_path)
        brown = features["brown_ratio"]
        yellow = features["yellow_ratio"]
        dark = features["dark_ratio"]
        green = features["green_ratio"]
        disease_score = brown + yellow + dark
        if green > 0.38 and disease_score < 0.18:
            return "Generic___Healthy", 0.72
        if dark > 0.18:
            return "Tomato___Late_blight", min(0.86, 0.58 + dark)
        if brown > 0.12 and yellow > 0.08:
            return "Tomato___Early_blight", min(0.84, 0.55 + brown + yellow / 2)
        if brown > 0.09:
            return "Rice___Brown_spot", min(0.8, 0.55 + brown)
        if yellow > 0.12:
            return "Wheat___Leaf_rust", min(0.78, 0.54 + yellow)
        return "Generic___Healthy", 0.62
