import chess
import chess.svg
import cairosvg
import os

# --- Configurações ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_FENS = os.path.join(BASE_DIR, "data", "fens_extraidos.txt")
PASTA_SAIDA = os.path.join(BASE_DIR, "data", "imagens_geradas")
LIMITE_IMAGENS = 200 # Vamos gerar poucas imagens no primeiro teste para ser rápido

# --- Lógica do Script ---

# 1. Verifica se o arquivo de FENs existe
if not os.path.exists(ARQUIVO_FENS):
    print(f"Erro: Arquivo de FENs '{ARQUIVO_FENS}' não encontrado.")
else:
    # 2. Cria a pasta de saída para as imagens se ela não existir
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        print(f"Pasta '{PASTA_SAIDA}' criada.")

    # 3. Abre o arquivo de FENs para leitura
    with open(ARQUIVO_FENS, "r") as fens_file:
        print(f"Lendo FENs de '{ARQUIVO_FENS}' e gerando imagens...")
        
        # Lê todas as linhas (todos os FENs) do arquivo
        fens = fens_file.readlines()
        
        # 4. Itera pela lista de FENs até o nosso limite
        for i, fen in enumerate(fens):
            if i >= LIMITE_IMAGENS:
                print(f"Limite de {LIMITE_IMAGENS} imagens atingido.")
                break

            # Remove espaços em branco e quebras de linha do FEN
            fen_limpo = fen.strip()
            
            try:
                # 5. Cria um objeto de tabuleiro a partir do FEN
                board = chess.Board(fen_limpo)
                
                # 6. Gera o código SVG para a imagem do tabuleiro
                # A função 'chess.svg.board' cria a imagem vetorial
                svg_code = chess.svg.board(board=board)
                
                # 7. Define o nome do arquivo de saída para a imagem
                nome_arquivo_saida = f"posicao_{i}.png"
                caminho_completo = os.path.join(PASTA_SAIDA, nome_arquivo_saida)
                
                # 8. Usa o cairosvg para converter o código SVG em um arquivo PNG
                cairosvg.svg2png(bytestring=svg_code, write_to=caminho_completo)

                # Imprime um progresso a cada 10 imagens
                if (i + 1) % 10 == 0:
                    print(f"  {i + 1}/{LIMITE_IMAGENS} imagens geradas...")

            except ValueError:
                print(f"Aviso: FEN inválido na linha {i+1}: '{fen_limpo}'. Pulando.")

    print("-" * 30)
    print("Geração de imagens concluída!")
    print(f"Verifique a pasta '{PASTA_SAIDA}'.")