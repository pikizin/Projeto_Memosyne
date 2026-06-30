# Projeto Memosyne

Este projeto tem como objetivo realizar o reconhecimento de posições de xadrez em imagens utilizando redes neurais convolucionais (CNNs). Ele processa dados de FENs, gera imagens de tabuleiros, fatia as casas e treina um modelo de deep learning capaz de classificar as peças.

## Estrutura do Repositório

- **src/**: Contém todos os scripts Python responsáveis pelo pipeline do projeto.
  - `01_extrator_fen.py`: Extrai FENs a partir de partidas em formato PGN.
  - `utils_gerador_imagens.py`: Converte os FENs extraídos em imagens de tabuleiro.
  - `02_construtor_dataset.py`: Constrói o dataset recortando e categorizando as imagens.
  - `utils_fatiador_tabuleiro.py`: Utilitário para fatiar um tabuleiro real em casas individuais.
  - `03_treinador_modelo.py`: Define e treina a rede neural CNN.
  - `04_reconhecedor.py`: Utiliza o modelo treinado para reconhecer peças em novas posições.
- **notebooks/**: Contém os Jupyter Notebooks utilizados para exploração e análise (ex: `ufabc-memosyne.ipynb`).
- **data/**: Contém os arquivos de dados (como `.pgn`, `.txt`, `.jpg`) e os datasets gerados (`dataset_final`).

## Requisitos

Instale as dependências necessárias através do arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Como Usar

Os scripts devem ser executados, preferencialmente, a partir do diretório raiz do projeto (embora as referências a arquivos tenham sido ajustadas para funcionar mesmo se executadas da pasta `src/`):

1. Extração de FENs:
   ```bash
   python src/01_extrator_fen.py
   ```
2. Geração das Imagens e do Dataset:
   ```bash
   python src/02_construtor_dataset.py
   ```
3. Treinamento do Modelo:
   ```bash
   python src/03_treinador_modelo.py
   ```
4. Reconhecimento a partir de uma nova imagem:
   ```bash
   python src/04_reconhecedor.py
   ```
