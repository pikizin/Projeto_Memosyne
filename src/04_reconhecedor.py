"""Inferência de peças de xadrez a partir de imagens de casas (64x64).

Exemplos:
  python src/04_reconhecedor.py --input data/casas_separadas_padronizadas
  python src/04_reconhecedor.py --input data/casas_separadas_padronizadas/casa_a8.png
"""
import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = BASE_DIR / "meu_modelo_de_xadrez_v2.keras"
DEFAULT_INPUT = BASE_DIR / "data" / "casas_separadas_padronizadas"
DATASET_DIR = BASE_DIR / "data" / "dataset_final"
IMG_SIZE = (64, 64)

def predict_image(model, path: Path, classes):
    img = tf.keras.utils.load_img(path, target_size=IMG_SIZE, color_mode="rgb")
    batch = np.expand_dims(tf.keras.utils.img_to_array(img), axis=0)
    probabilities = model.predict(batch, verbose=0)[0]
    if len(probabilities) != len(classes):
        raise ValueError("Número de classes do modelo difere do dataset; use o mesmo dataset do treinamento.")
    idx = int(np.argmax(probabilities))
    return classes[idx], float(probabilities[idx])

def main():
    parser = argparse.ArgumentParser(description="Classificar peças em imagens de casas de xadrez")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Imagem ou pasta com imagens de casas")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL, help="Arquivo .keras treinado")
    args = parser.parse_args()

    if not args.model.is_file():
        parser.error(f"Modelo não encontrado: {args.model}. Execute antes src/03_treinador_modelo.py")
    if not DATASET_DIR.is_dir():
        parser.error(f"Dataset não encontrado: {DATASET_DIR} (necessário para identificar as classes).")
    classes = sorted(p.name for p in DATASET_DIR.iterdir() if p.is_dir())
    if not classes:
        parser.error("Não existem pastas de classes no dataset.")

    model = tf.keras.models.load_model(args.model)
    if args.input.is_file():
        files = [args.input]
    elif args.input.is_dir():
        files = sorted(p for p in args.input.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"})
    else:
        parser.error(f"Entrada não encontrada: {args.input}")
    if not files:
        parser.error("Nenhuma imagem encontrada.")

    predictions = {}
    for path in files:
        label, confidence = predict_image(model, path, classes)
        print(f"{path.name}: {label} ({confidence:.1%})")
        predictions[path.stem.lower()] = label

    # Constrói FEN somente se existirem exatamente as 64 casas nomeadas casa_a8 ... casa_h1.
    expected = {f"casa_{chr(97 + col)}{row}" for row in range(1, 9) for col in range(8)}
    mapping = {"wP": "P", "wN": "N", "wB": "B", "wR": "R", "wQ": "Q", "wK": "K",
               "bP": "p", "bN": "n", "bB": "b", "bR": "r", "bQ": "q", "bK": "k", "empty": None}
    if set(predictions) == expected and all(c in mapping for c in predictions.values()):
        ranks = []
        for row in range(8, 0, -1):
            rank, empties = "", 0
            for col in range(8):
                symbol = mapping[predictions[f"casa_{chr(97 + col)}{row}"]]
                if symbol is None:
                    empties += 1
                else:
                    if empties:
                        rank += str(empties)
                        empties = 0
                    rank += symbol
            if empties:
                rank += str(empties)
            ranks.append(rank)
        print("FEN (apenas posicionamento):", "/".join(ranks))

if __name__ == "__main__":
    main()
