import cv2
import os

# Nome da imagem de entrada e da pasta de saída
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGEM_ENTRADA = os.path.join(BASE_DIR, "data", "tabuleiro_cortado.jpg")
PASTA_SAIDA = os.path.join(BASE_DIR, "data", "casas_separadas_padronizadas")
MARGEM = 2
TAMANHO_PADRAO = 800 # Definimos um tamanho fixo e quadrado

# Margem (em pixels) para cortar dentro de cada casa
MARGEM = 6  # Ajuste este valor conforme necessário

# 1. Criar a pasta de saída se ela não existir
if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)
    print(f"Pasta '{PASTA_SAIDA}' criada com sucesso.")

# 2. Carregar a imagem do tabuleiro já cortado
imagem = cv2.imread(IMAGEM_ENTRADA)

if imagem is None:
    print(f"Erro: não foi possível carregar a imagem '{IMAGEM_ENTRADA}'.")
    print("Verifique se o arquivo existe e está na pasta correta.")
else:
    # 3. Obter as dimensões da imagem
    altura, largura, _ = imagem.shape
    print(f"Imagem carregada ({largura}x{altura} pixels).")

    # 4. Calcular o tamanho de cada casa (assumindo um tabuleiro 8x8)
    tamanho_casa_largura = largura // 8
    tamanho_casa_altura = altura // 8

    print("Fatiando o tabuleiro em 64 casas (com margem de segurança)...")

    # 5. Iterar pelas 8 linhas e 8 colunas do tabuleiro
    for i in range(8):  # i representa a linha (de 0 a 7)
        for j in range(8):  # j representa a coluna (de 0 a 7)
            
            # 6. Calcular as coordenadas para cortar cada casa COM MARGEM
            y1 = i * tamanho_casa_altura + MARGEM
            y2 = (i + 1) * tamanho_casa_altura - MARGEM
            x1 = j * tamanho_casa_largura + MARGEM
            x2 = (j + 1) * tamanho_casa_largura - MARGEM

            # 7. Usar o fatiamento (slicing) do NumPy para extrair a imagem da casa
            casa_img = imagem[y1:y2, x1:x2]

            # 8. Criar um nome de arquivo descritivo
            nome_arquivo = f"casa_{chr(ord('a') + j)}{8 - i}.png"
            caminho_completo = os.path.join(PASTA_SAIDA, nome_arquivo)

            # 9. Salvar a imagem da casa na pasta de saída
            cv2.imwrite(caminho_completo, casa_img)
    
    print("-" * 30)
    print("Processo concluído com sucesso!")
    
    # CORREÇÃO AQUI: Usando a variável correta 'PASTA_SAIDA'
    print(f"Verifique a pasta '{PASTA_SAIDA}' para ver as 64 imagens geradas.")