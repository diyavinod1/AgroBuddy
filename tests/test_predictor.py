from pathlib import Path

import cv2
import numpy as np

from ml.inference.predictor import PlantDiseasePredictor


def test_predictor_heuristic_runs(tmp_path: Path) -> None:
    image = np.zeros((224, 224, 3), dtype=np.uint8)
    image[:, :] = (40, 120, 40)
    image_path = tmp_path / "leaf.jpg"
    cv2.imwrite(str(image_path), image)
    result = PlantDiseasePredictor().predict(image_path)
    assert result.crop_name
    assert 0 <= result.confidence <= 1
