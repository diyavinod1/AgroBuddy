from pathlib import Path

import cv2
import numpy as np


class ImagePreprocessor:
    def __init__(self, image_size: tuple[int, int] = (224, 224)) -> None:
        self.image_size = image_size

    def load_bgr(self, image_path: str | Path) -> np.ndarray:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        return image

    def preprocess(self, image_path: str | Path) -> np.ndarray:
        image = self.load_bgr(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, self.image_size)
        normalized = resized.astype("float32") / 255.0
        return np.expand_dims(normalized, axis=0)

    def leaf_features(self, image_path: str | Path) -> dict[str, float]:
        image = self.load_bgr(image_path)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, (25, 35, 35), (95, 255, 255))
        yellow_mask = cv2.inRange(hsv, (15, 40, 40), (35, 255, 255))
        brown_mask = cv2.inRange(hsv, (5, 40, 20), (25, 255, 210))
        dark_mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 70))
        total = float(image.shape[0] * image.shape[1])
        return {
            "green_ratio": float(np.count_nonzero(green_mask) / total),
            "yellow_ratio": float(np.count_nonzero(yellow_mask) / total),
            "brown_ratio": float(np.count_nonzero(brown_mask) / total),
            "dark_ratio": float(np.count_nonzero(dark_mask) / total),
        }
