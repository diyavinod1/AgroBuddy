from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


def build_grad_cam(model: tf.keras.Model, batch: np.ndarray, source_image_path: str | Path, output_path: str | Path) -> str | None:
    conv_layers = [layer for layer in model.layers if hasattr(layer, "output") and len(layer.output.shape) == 4]
    if not conv_layers:
        return None
    last_conv_layer = conv_layers[-1]
    grad_model = tf.keras.models.Model(model.inputs, [last_conv_layer.output, model.output])
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(batch)
        class_index = tf.argmax(predictions[0])
        class_channel = predictions[:, class_index]
    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap_np = heatmap.numpy()

    image = cv2.imread(str(source_image_path))
    if image is None:
        return None
    heatmap_np = cv2.resize(heatmap_np, (image.shape[1], image.shape[0]))
    heatmap_np = np.uint8(255 * heatmap_np)
    colored = cv2.applyColorMap(heatmap_np, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(image, 0.65, colored, 0.35, 0)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output), overlay)
    return str(output)
