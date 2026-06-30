# Documentação Teórica: Machine Learning e Visão Computacional

Este documento serve como um guia para ajudar a entender os conceitos por trás do **Projeto Memosyne**, onde utilizamos Inteligência Artificial para olhar para uma imagem de um tabuleiro de xadrez e descobrir quais peças estão em cada casa.

---

## 1. Visão Computacional (Computer Vision)
A Visão Computacional é um campo da Inteligência Artificial (IA) que ensina os computadores a "enxergarem" e interpretarem imagens e vídeos do mundo real, de forma semelhante (ou até superior) à visão humana.

Para o computador, uma imagem não passa de uma grande matriz (tabela) de números, onde cada número representa a cor e o brilho de um pequeno ponto chamado pixel. O objetivo da Visão Computacional, neste projeto, é analisar essa tabela de pixels e identificar um padrão: *"Ah, estes pixels formam um Cavalo Branco"* ou *"Isto é uma casa vazia"*.

---

## 2. Machine Learning e Redes Neurais Convolucionais (CNNs)
**Machine Learning (Aprendizado de Máquina)** é a ideia de que, em vez de darmos regras fixas para o computador (ex: *"se tiver um formato assim, é um peão"*), nós mostramos **milhares de exemplos** e ele aprende sozinho a reconhecer os padrões.

No Projeto Memosyne, utilizamos uma **Rede Neural Convolucional (CNN)**. As CNNs são arquiteturas de redes neurais inspiradas no córtex visual dos animais, extremamente poderosas para imagens. Elas usam "filtros convolucionais" que varrem a imagem procurando padrões básicos (como linhas e bordas) e, nas camadas mais profundas, combinam essas bordas para formar conceitos complexos (como o formato de uma peça de xadrez).

---

## 3. Conceitos Fundamentais do Treinamento

Quando nosso código em `03_treinador_modelo.py` está rodando, ele está ajustando o cérebro da nossa inteligência artificial. Abaixo estão os termos mais importantes que aparecem no terminal durante esse processo:

### Pesos (Weights)
Imagine que a rede neural seja composta por várias "chaves" (sinapses) que ligam um neurônio ao outro. O "peso" é a força dessa ligação. No início do treinamento, esses pesos são aleatórios. Conforme o computador acerta ou erra ao adivinhar as peças de xadrez, ele **ajusta esses pesos** para melhorar os palpites futuros. "Aprender", no contexto de IA, significa encontrar a combinação ideal de pesos.

### Época (Epoch)
Uma época (**Epoch**) acontece quando a rede neural já viu e analisou **todas** as imagens de treinamento do nosso dataset exatamente uma vez. 
Se configurarmos o código para 20 Epochs, significa que a IA vai estudar a apostila inteira 20 vezes. Cada vez que ela relê o material, ela ajusta seus *pesos* e fica um pouco mais inteligente. 

### Loss (Perda ou Erro)
O **Loss** é a métrica que diz "o quão errado o modelo está". 
- Se a IA olha para uma imagem de um *Bispo*, mas tem quase certeza que é um *Peão*, o Loss será **alto**. 
- Se ela disser que é um Bispo com muita convicção, o Loss será **baixo**. 
O objetivo principal do treinamento é sempre **reduzir a Loss (minimizar o erro)** o máximo possível.

### Accuracy (Acurácia)
Enquanto a Loss mede a margem de erro matemático, a **Acurácia (Accuracy)** é muito mais simples: qual a porcentagem de peças que ela acertou? Se a acurácia está em 0.95, significa que ela acerta 95% das casas do tabuleiro.

### Validation Loss (val_loss) e Validation Accuracy (val_accuracy)
Durante o estudo, nós separamos 20% das imagens do dataset e as escondemos da IA (este é o Validation Set, ou Grupo de Validação). A IA só treina nos outros 80%.

No final de cada **Epoch**, testamos a IA com essas imagens escondidas que ela nunca viu.
- **val_loss**: O erro da IA nas imagens que ela nunca viu.
- **val_accuracy**: A porcentagem de acertos nas imagens que ela nunca viu.

**Por que isso é essencial?**
Para evitar o **Overfitting** (Decoreba). Se a `accuracy` normal estiver em 99% (a IA acerta tudo do grupo de treino), mas a `val_accuracy` travar em 60%, significa que a IA apenas *decorou* as imagens específicas de treino, mas não aprendeu realmente como é uma peça de xadrez genérica. Ela está falhando nas imagens novas. O que realmente importa para nós é o `val_accuracy`.
