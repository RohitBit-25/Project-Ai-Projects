import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras.optimizers import RMSprop

# Load and preprocess the dataset
filepath = tf.keras.utils.get_file('shakespeare.txt',
                                   'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')

text = open(filepath,'rb').read().decode(encoding='utf-8').lower()

text = text[300000:800000]  # Use a subset of the text for faster training

characters = sorted(set(text)) # filter out all the unique characters in the text

char_to_index = dict((c, i) for i, c in enumerate(characters)) # assign one number to each character

index_to_char = dict((i, c) for i, c in enumerate(characters)) # reverse mapping

SEQ_LENGTH = 40
STEP_SIZE= 3

sentences =[]

next_characters =[]

for i in range(0, len(text) - SEQ_LENGTH, STEP_SIZE):
    sentences.append(text[i: i + SEQ_LENGTH])
    next_characters.append(text[i + SEQ_LENGTH])


# Create one-hot encoded input and output arrays. Use a shape tuple and the builtin bool to avoid
# deprecated numpy aliases (np.bool / np.bool_).
x = np.zeros((len(sentences), SEQ_LENGTH, len(characters)), dtype=bool)
y = np.zeros((len(sentences), len(characters)), dtype=bool)

for i, sentence in enumerate(sentences):
    for t, character in enumerate(sentence):
        x[i, t, char_to_index[character]] = 1
    y[i, char_to_index[next_characters[i]]] = 1
def load_model_or_exit(path='shakespeare_model.h5'):
    try:
        return tf.keras.models.load_model(path)
    except Exception as e:
        print(f"Failed to load model '{path}': {e}")
        raise SystemExit(1)


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-10) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_text(model, length=400, temperature=1.0, seed_text=None):
    if seed_text is None:
        start_index = random.randint(0, len(text) - SEQ_LENGTH - 1)
        generated_text = text[start_index: start_index + SEQ_LENGTH]
    else:
        generated_text = seed_text[-SEQ_LENGTH:]

    print("Generating with seed: " + generated_text)

    for i in range(length):
        sampled = np.zeros((1, SEQ_LENGTH, len(characters)), dtype=bool)
        for t, char in enumerate(generated_text[-SEQ_LENGTH:]):
            sampled[0, t, char_to_index[char]] = 1

        preds = model.predict(sampled, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_char = index_to_char[next_index]

        generated_text += next_char

    return generated_text


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate text from a trained character-RNN model')
    parser.add_argument('--model', default='shakespeare_model.h5', help='Path to saved model')
    parser.add_argument('--length', type=int, default=400, help='Number of characters to generate')
    parser.add_argument('--temperature', type=float, default=1.0, help='Sampling temperature')
    parser.add_argument('--seed', type=str, default=None, help='Optional seed text (will be truncated/padded to sequence length)')
    args = parser.parse_args()

    model = load_model_or_exit(args.model)

    for temp in [args.temperature]:
        out = generate_text(model, length=args.length, temperature=temp, seed_text=args.seed)
        print('\n' + out + '\n')


if __name__ == '__main__':
    main()


