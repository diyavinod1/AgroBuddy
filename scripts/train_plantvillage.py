import argparse
import json
from pathlib import Path

import tensorflow as tf
from tensorflow import keras


def train(data_dir: Path, output_model: Path, output_labels: Path, epochs: int, image_size: int, batch_size: int) -> None:
    train_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=(image_size, image_size),
        batch_size=batch_size,
    )
    val_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=(image_size, image_size),
        batch_size=batch_size,
    )
    labels = train_ds.class_names
    augmentation = keras.Sequential(
        [
            keras.layers.RandomFlip("horizontal"),
            keras.layers.RandomRotation(0.08),
            keras.layers.RandomZoom(0.12),
            keras.layers.RandomContrast(0.1),
        ]
    )
    base = keras.applications.MobileNetV2(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False
    inputs = keras.Input(shape=(image_size, image_size, 3))
    x = augmentation(inputs)
    x = keras.applications.mobilenet_v2.preprocess_input(x * 255.0)
    x = base(x, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.25)(x)
    outputs = keras.layers.Dense(len(labels), activation="softmax")(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(train_ds, validation_data=val_ds, epochs=epochs)
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False
    model.compile(optimizer=keras.optimizers.Adam(1e-5), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(train_ds, validation_data=val_ds, epochs=max(2, epochs // 2))
    output_model.parent.mkdir(parents=True, exist_ok=True)
    output_labels.parent.mkdir(parents=True, exist_ok=True)
    model.save(output_model)
    output_labels.write_text(json.dumps(labels, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train AgroBuddy PlantVillage transfer-learning classifier.")
    parser.add_argument("--data-dir", required=True, type=Path, help="Directory containing one folder per disease class.")
    parser.add_argument("--output-model", default=Path("models/plant_disease_model.keras"), type=Path)
    parser.add_argument("--output-labels", default=Path("models/labels.json"), type=Path)
    parser.add_argument("--epochs", default=8, type=int)
    parser.add_argument("--image-size", default=224, type=int)
    parser.add_argument("--batch-size", default=32, type=int)
    args = parser.parse_args()
    train(args.data_dir, args.output_model, args.output_labels, args.epochs, args.image_size, args.batch_size)


if __name__ == "__main__":
    main()
