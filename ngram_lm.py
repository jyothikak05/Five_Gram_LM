
import random
import re
from collections import defaultdict, Counter

N = 5

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    return tokens

def build_ngram_model(tokens, n=5):
    model = defaultdict(Counter)
    for i in range(len(tokens) - n):
        context = tuple(tokens[i:i+n-1])
        target = tokens[i+n-1]
        model[context][target] += 1
    return model

def generate_text(model, seed, length=50):
    seed_tokens = preprocess(seed)
    if len(seed_tokens) < N-1:
        raise ValueError(f"Seed must have at least {N-1} words")

    context = tuple(seed_tokens[-(N-1):])
    output = seed_tokens[:]

    for _ in range(length):
        if context not in model:
            break
        next_word = random.choices(
            list(model[context].keys()),
            weights=model[context].values()
        )[0]
        output.append(next_word)
        context = tuple(output[-(N-1):])

    return " ".join(output)

if __name__ == "__main__":
    with open("pridenprejudice.txt", "r", encoding="utf-8") as f:
        text = f.read()

    tokens = preprocess(text)
    model = build_ngram_model(tokens, N)

    seeds = [
        "it was a very",
        "she could not help",
        "it was impossible to"
    ]

    for s in seeds:
        print("\nSeed:", s)
        print(generate_text(model, s, 40))
