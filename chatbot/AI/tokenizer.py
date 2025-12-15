import json
import re

class SimpleTokenizer:
    def __init__(self):
        self.word_index = {}
        self.index_word = {}
        self.num_words = 0

    def fit_on_text(self, text):
        # Simple split by whitespace and punctuation
        words = re.findall(r'\w+', text.lower())
        for w in words:
            if w not in self.word_index:
                self.word_index[w] = self.num_words
                self.index_word[self.num_words] = w
                self.num_words += 1

    def texts_to_sequences(self, texts):
        sequences = []
        for text in texts:
            words = re.findall(r'\w+', text.lower())
            seq = [self.word_index.get(w, 0) for w in words if w in self.word_index]
            sequences.append(seq)
        return sequences

    def sequences_to_texts(self, sequences):
        texts = []
        for seq in sequences:
            words = [self.index_word.get(i, "") for i in seq]
            texts.append(" ".join(words))
        return texts

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({
                "word_index": self.word_index,
                "index_word": self.index_word,
                "num_words": self.num_words
            }, f)

    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            self.word_index = data["word_index"]
            self.index_word = {int(k): v for k, v in data["index_word"].items()}
            self.num_words = data["num_words"]
