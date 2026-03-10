"""Script para ejecutar el entrenamiento del mini-GPT directamente (sin Jupyter overhead)."""

import json
import numpy as np
import tensorflow as tf
import keras
from keras import layers

print("GPU disponible:", tf.config.list_physical_devices('GPU'))

# --- Parte 2: Tokenizacion ---
with open('titulares.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Caracteres totales: {len(text)}")
print(f"Titulares (aprox): {text.count(chr(10))}")

vocab = sorted(set(text))
vocab_size = len(vocab)
print(f"Vocabulario: {vocab_size} caracteres unicos")

char_to_idx = {ch: i for i, ch in enumerate(vocab)}
idx_to_char = {i: ch for i, ch in enumerate(vocab)}

def encode(s):
    return [char_to_idx[c] for c in s]

def decode(ids):
    return ''.join([idx_to_char[i] for i in ids])

# --- Parte 3: Datos ---
SEQ_LENGTH = 80
BATCH_SIZE = 64

tokens = np.array(encode(text))
print(f"Tokens totales: {tokens.shape[0]}")

def crear_secuencias(tokens, seq_len):
    X, y = [], []
    for i in range(len(tokens) - seq_len):
        X.append(tokens[i:i + seq_len])
        y.append(tokens[i + 1:i + seq_len + 1])
    return np.array(X), np.array(y)

X, y = crear_secuencias(tokens, SEQ_LENGTH)
print(f"Secuencias: {X.shape}")

dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(10000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# --- Parte 4: Componentes ---
class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super().__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, dropout=0.1):
        super().__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation="gelu"),
            layers.Dense(embed_dim),
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout)
        self.dropout2 = layers.Dropout(dropout)

    def causal_attention_mask(self, batch_size, seq_len):
        i = tf.range(seq_len)[:, tf.newaxis]
        j = tf.range(seq_len)
        mask = tf.cast(i >= j, dtype=tf.float32)
        mask = tf.reshape(mask, [1, 1, seq_len, seq_len])
        return tf.tile(mask, [batch_size, 1, 1, 1])

    def call(self, inputs, training=False):
        batch_size = tf.shape(inputs)[0]
        seq_len = tf.shape(inputs)[1]
        mask = self.causal_attention_mask(batch_size, seq_len)
        attn_output = self.att(inputs, inputs, attention_mask=mask)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

# --- Parte 5: Modelo (reducido para CPU) ---
EMBED_DIM = 128
NUM_HEADS = 4
FF_DIM = 256
NUM_BLOCKS = 2

def crear_modelo():
    inputs = layers.Input(shape=(SEQ_LENGTH,), dtype=tf.int32)
    x = TokenAndPositionEmbedding(SEQ_LENGTH, vocab_size, EMBED_DIM)(inputs)
    for _ in range(NUM_BLOCKS):
        x = TransformerBlock(EMBED_DIM, NUM_HEADS, FF_DIM)(x)
    outputs = layers.Dense(vocab_size, activation="softmax")(x)
    return keras.Model(inputs=inputs, outputs=outputs)

model = crear_modelo()
model.summary()

# --- Parte 6: Entrenamiento ---
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

callbacks = [
    keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2),
]

history = model.fit(dataset, epochs=15, callbacks=callbacks)

# Guardar history
history_data = {k: [float(v) for v in vals] for k, vals in history.history.items()}
with open('training_history.json', 'w') as f:
    json.dump(history_data, f)
print("History guardado en training_history.json")

# --- Parte 7: Generacion ---
def generar_texto(model, inicio, longitud=100, temperatura=1.0):
    generado = list(encode(inicio))
    for _ in range(longitud):
        input_seq = generado[-SEQ_LENGTH:]
        input_seq = np.array(input_seq)[np.newaxis, :]
        if len(input_seq[0]) < SEQ_LENGTH:
            pad_len = SEQ_LENGTH - len(input_seq[0])
            input_seq = np.pad(input_seq, ((0, 0), (pad_len, 0)))
        preds = model.predict(input_seq, verbose=0)[0, -1, :]
        preds = np.log(preds + 1e-10) / temperatura
        preds = np.exp(preds) / np.sum(np.exp(preds))
        next_idx = np.random.choice(len(preds), p=preds)
        generado.append(next_idx)
        if idx_to_char[next_idx] == '\n':
            break
    return decode(generado)

# Generacion con temperaturas
results = {}
print("\n" + "=" * 60)
print("GENERACION CON DIFERENTES TEMPERATURAS")
print("=" * 60)

for temp in [0.5, 1.0, 1.5]:
    print(f"\n--- Temperatura {temp} ---")
    results[str(temp)] = []
    for i in range(3):
        resultado = generar_texto(model, "el gobierno ", temperatura=temp)
        print(f"  {i+1}. {resultado.strip()}")
        results[str(temp)].append(resultado.strip())

# Generacion con diferentes inicios
print("\n" + "=" * 60)
print("GENERACION CON DIFERENTES INICIOS (temperatura=0.8)")
print("=" * 60)

inicios = ["la economia ", "un nuevo ", "el presidente ", "argentina ", "se espera "]
results_inicios = {}
for inicio in inicios:
    print(f"\nInicio: '{inicio}'")
    results_inicios[inicio] = []
    for i in range(3):
        resultado = generar_texto(model, inicio, temperatura=0.8)
        print(f"  {i+1}. {resultado.strip()}")
        results_inicios[inicio].append(resultado.strip())

# Guardar resultados de generacion
with open('generation_results.json', 'w', encoding='utf-8') as f:
    json.dump({'temperatures': results, 'inicios': results_inicios}, f, ensure_ascii=False, indent=2)

print("\nResultados guardados en generation_results.json")
print("COMPLETADO.")
