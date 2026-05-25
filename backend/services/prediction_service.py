from pathlib import Path

from backend.database.repositories import PredictionRepository
from backend.models.domain import PredictionResult
from backend.services.user_service import UserService
from ml.inference.predictor import PlantDiseasePredictor


class PredictionService:
    def __init__(
        self,
        predictor: PlantDiseasePredictor | None = None,
        users: UserService | None = None,
        predictions: PredictionRepository | None = None,
    ) -> None:
        self.predictor = predictor or PlantDiseasePredictor()
        self.users = users or UserService()
        self.predictions = predictions or PredictionRepository()

    def predict_for_user(self, telegram_user_id: int, image_path: str | Path) -> PredictionResult:
        user = self.users.get_user(telegram_user_id) or self.users.ensure_user(telegram_user_id)
        result = self.predictor.predict(image_path)
        self.predictions.create(
            user_id=user["id"],
            image_path=str(image_path),
            crop_name=result.crop_name,
            disease_name=result.disease_name,
            confidence=result.confidence,
            remedies=result.remedies,
            fertilizer=result.fertilizer,
            prevention=result.prevention,
        )
        return result
