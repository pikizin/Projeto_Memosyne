import chess
import chess.svg
import cairosvg
import os
import cv2
import numpy as np
import random

# --- Configurações ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_FENS = os.path.join(BASE_DIR, "data", "fens_extraidos.txt")
PASTA_DATASET = os.path.join(BASE_DIR, "data", "dataset_final")
LIMITE_FENS_PARA_PROCESSAR = 4000
TAMANHO_IMAGEM_SAIDA = 64
MARGEM_FATIAMENTO = 2

cores_possiveis = [
    {"square light": "#f2d3b1", "square dark": "#a97b65"},
    {"square light": "#e8ebf0", "square dark": "#7d8796"},
    {"square light": "#ffffff", "square dark": "#404040"},
    {"square light": "#baca44", "square dark": "#718339"},
    {"square light": "#f7f7f7", "square dark": "#8c8c8c"},
]

# --- Lógica do Script ---

pecas_map = {
    'P': 'wP', 'p': 'bP', 'N': 'wN', 'n': 'bN', 'B': 'wB', 'b': 'bB',
    'R': 'wR', 'r': 'bR', 'Q': 'wQ', 'q': 'bQ', 'K': 'wK', 'k': 'bK'
}
nomes_pastas = list(pecas_map.values()) + ['empty']

print(f"Criando estrutura de pastas do dataset em '{PASTA_DATASET}'...")
for nome_pasta in nomes_pastas:
    caminho_pasta = os.path.join(PASTA_DATASET, nome_pasta)
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

contadores_pecas = {nome: 0 for nome in nomes_pastas}

print(f"Lendo FENs de '{ARQUIVO_FENS}'...")
with open(ARQUIVO_FENS, "r") as f:
    fens = f.readlines()

print(f"Iniciando processamento de {LIMITE_FENS_PARA_PROCESSAR} FENs...")
for i, fen in enumerate(fens):
    if i >= LIMITE_FENS_PARA_PROCESSAR:
        print(f"Limite de {LIMITE_FENS_PARA_PROCESSAR} FENs atingido.")
        break

    fen_limpo = fen.strip()
    try:
        board = chess.Board(fen_limpo)
        
        cores_aleatorias = random.choice(cores_possiveis)
        svg_code = chess.svg.board(board=board, size=400, colors=cores_aleatorias)
        png_bytes = cairosvg.svg2png(bytestring=svg_code)

        np_array = np.frombuffer(png_bytes, np.uint8)
        imagem_tabuleiro = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        altura, largura, _ = imagem_tabuleiro.shape
        tamanho_casa = largura // 8
        
        for linha in range(8):
            for coluna in range(8):
                y1 = linha * tamanho_casa + MARGEM_FATIAMENTO
                y2 = (linha + 1) * tamanho_casa - MARGEM_FATIAMENTO
                x1 = coluna * tamanho_casa + MARGEM_FATIAMENTO
                x2 = (coluna + 1) * tamanho_casa - MARGEM_FATIAMENTO
                
                img_casa = imagem_tabuleiro[y1:y2, x1:x2]
                img_casa_redimensionada = cv2.resize(img_casa, (TAMANHO_IMAGEM_SAIDA, TAMANHO_IMAGEM_SAIDA))

                quadrado = chess.square(coluna, 7 - linha)
                peca = board.piece_at(quadrado)
                
                if peca is not None:
                    nome_pasta_peca = pecas_map[peca.symbol()]
                else:
                    nome_pasta_peca = 'empty'
                
                contadores_pecas[nome_pasta_peca] += 1
                nome_arquivo = f"{contadores_pecas[nome_pasta_peca]:04d}.png"
                caminho_final = os.path.join(PASTA_DATASET, nome_pasta_peca, nome_arquivo)
                cv2.imwrite(caminho_final, img_casa_redimensionada)
        
        # --- LINHA DE PROGRESSO RESTAURADA AQUI ---
        if (i + 1) % 50 == 0:
            print(f"  Processados {i + 1}/{LIMITE_FENS_PARA_PROCESSAR} FENs...")

    except Exception as e:
        print(f"Erro ao processar FEN na linha {i+1}: '{fen_limpo}'. Erro: {e}")


print("-" * 30)
print("Criação do novo dataset concluída!")
print(f"Verifique a pasta '{PASTA_DATASET}'.")