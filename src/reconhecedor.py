import tensorflow as tf
import tensorflow.keras as keras
import os

# --- 1. PARÂMETROS DE CONFIGURAÇÃO ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "data", "dataset_final")
IMG_SIZE = (64, 64)
BATCH_SIZE = 329
EPOCHS = 20  # Aumentei um pouco as épocas para dar mais tempo ao modelo maior

# --- 2. CARREGAR E PREPARAR OS DADOS ---
print("Carregando e preparando o dataset...")

train_ds = keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
    # Removido label_mode para usar o padrão int
)

val_ds = keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
assert class_names is not None
num_classes = len(class_names)
print(f"Encontradas {num_classes} classes: {class_names}")

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# --- 3. CONSTRUIR A ARQUITETURA DA REDE NEURAL (CNN) ---
print("Construindo o modelo da CNN (versão aprimorada)...")

data_augmentation = keras.Sequential(
    [
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.1),
        keras.layers.RandomZoom(0.1),
        keras.layers.RandomContrast(0.1),  # Ajuda na confusão de cores
        keras.layers.RandomBrightness(0.1)  # Ajuda com variações de iluminação
    ],
    name="data_augmentation",
)

model = keras.Sequential([
    data_augmentation,
    keras.layers.Rescaling(1./255),
    keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Dropout(0.20),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(num_classes, activation='softmax')
])

# --- 4. COMPILAR O MODELO ---
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',  # Ajustado para labels inteiros
    metrics=['accuracy']
)

model.summary()

# --- 5. TREINAR O MODELO ---
print("\nIniciando o treinamento do modelo APRIMORADO...")
print(f"O treinamento ocorrerá por {EPOCHS} épocas.")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

print("\nTreinamento concluído!")

# --- 6. SALVAR O MODELO TREINADO ---
model.save('meu_modelo_de_xadrez_v2.keras')
print("\nModelo aprimorado salvo com sucesso como 'meu_modelo_de_xadrez_v2.keras'")
