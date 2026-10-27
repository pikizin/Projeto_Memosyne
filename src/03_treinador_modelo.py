"""Treinamento da CNN de classificação de casas de xadrez."""
import os
from pathlib import Path

import tensorflow as tf
from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "data" / "dataset_final"
MODEL_PATH = BASE_DIR / "meu_modelo_de_xadrez_v2.keras"
IMG_SIZE = (64, 64)
BATCH_SIZE = 32
EPOCHS = 20
SEED = 123

def main():
    if not DATASET_DIR.is_dir():
        raise FileNotFoundError(f"Dataset não encontrado: {DATASET_DIR}")
    train_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIR, validation_split=0.2, subset="training",
        seed=SEED, image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="categorical"
    )
    val_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIR, validation_split=0.2, subset="validation",
        seed=SEED, image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="categorical"
    )
    classes = train_ds.class_names
    print("Classes:", classes)
    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)

    # Sem flip/rotação por padrão: podem alterar artificialmente a orientação das peças.
    augmentation = keras.Sequential([
        keras.layers.RandomContrast(0.1),
        keras.layers.RandomBrightness(0.1),
    ], name="augmentation")

    model = keras.Sequential([
        keras.Input(shape=(*IMG_SIZE, 3)),
        augmentation,
        keras.layers.Rescaling(1.0 / 255),
        keras.layers.Conv2D(16, 3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(32, 3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(64, 3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(),
        keras.layers.Dropout(0.2),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(len(classes), activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
    model.save(MODEL_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")

if __name__ == "__main__":
    main()
