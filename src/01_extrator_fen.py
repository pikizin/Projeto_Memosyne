import chess.pgn
import os

# --- Configurações ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOME_ARQUIVO_PGN = os.path.join(BASE_DIR, "data", "Morphy.pgn")
NOME_ARQUIVO_SAIDA = os.path.join(BASE_DIR, "data", "fens_extraidos.txt")
LIMITE_DE_FENS = 20000  # Limite para não gerar um arquivo gigante no primeiro teste

# --- Lógica do Script ---

# 1. Verifica se o arquivo PGN existe
if not os.path.exists(NOME_ARQUIVO_PGN):
    print(f"Erro: Arquivo PGN '{NOME_ARQUIVO_PGN}' não encontrado.")
    print("Por favor, baixe o arquivo e coloque na mesma pasta do script.")
else:
    # 2. Abre o arquivo PGN para leitura
    pgn_file = open(NOME_ARQUIVO_PGN)
    
    # Prepara o arquivo de saída para escrever os FENs
    output_file = open(NOME_ARQUIVO_SAIDA, "w")
    
    print(f"Lendo jogos de '{NOME_ARQUIVO_PGN}'...")
    print(f"Vamos extrair no máximo {LIMITE_DE_FENS} posições (FENs).")
    
    fen_count = 0
    game_count = 0

    # 3. Loop principal: lê um jogo do arquivo PGN de cada vez
    # A sintaxe `:=` (operador Walrus) permite ler e verificar na mesma linha
    while (game := chess.pgn.read_game(pgn_file)):
        if fen_count >= LIMITE_DE_FENS:
            print(f"Limite de {LIMITE_DE_FENS} FENs atingido. Encerrando.")
            break
            
        game_count += 1
        print(f"Processando jogo #{game_count}...")
        
        # 4. Pega o tabuleiro na posição inicial do jogo
        board = game.board()
        
        # 5. Itera por todos os lances da partida principal
        for move in game.mainline_moves():
            # Aplica o lance no tabuleiro interno
            board.push(move)
            
            # Converte a posição atual do tabuleiro para a notação FEN
            fen = board.fen()
            
            # Escreve o FEN em uma nova linha no nosso arquivo de saída
            output_file.write(fen + "\n")
            
            fen_count += 1
            
            # Interrompe o loop interno se o limite for atingido
            if fen_count >= LIMITE_DE_FENS:
                break
    
    # 6. Fecha os arquivos que abrimos
    pgn_file.close()
    output_file.close()

    print("-" * 30)
    print("Extração concluída!")
    print(f"Total de {game_count} jogos processados.")
    print(f"Total de {fen_count} FENs extraídos.")
    print(f"Os FENs foram salvos no arquivo: '{NOME_ARQUIVO_SAIDA}'")