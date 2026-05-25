import json
from pathlib import Path
from typing import Any

import numpy as np
from tensorflow import keras

from backend.core.config import Settings, get_settings
from ml.knowledge_base import DISEASE_KNOWLEDGE


class PlantDiseaseModel:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.model: Any | None = None
        self.labels = list(DISEASE_KNOWLEDGE.keys())
        self._load_labels()
        self._load_model()

    def _load_labels(self) -> None:
        path = Path(self.settings.model_labels_path)
        if path.exists():
            self.labels = json.loads(path.read_text(encoding="utf-8"))

    def _load_model(self) -> None:
        path = Path(self.settings.model_path)
        if path.exists():
            self.model = keras.models.load_model(path)

    @property
    def has_trained_model(self) -> bool:
        return self.model is not None

    def predict(self, batch: np.ndarray) -> tuple[str, float, np.ndarray | None]:
        if self.model is None:
            raise RuntimeError("No trained model loaded")
        probabilities = self.model.predict(batch, verbose=0)[0]
        index = int(np.argmax(probabilities))
        label = self.labels[index] if index < len(self.labels) else self.labels[0]
        return label, float(probabilities[index]), probabilities
