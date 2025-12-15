import requests
from chatbot.AI.tokenizer import SimpleTokenizer

class TextLoader:
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer if tokenizer else SimpleTokenizer()
        self.data = []

    def load_from_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        self.data.append(text)
        return text

    def load_from_url(self, url):
        try:
            response = requests.get(url)
            text = response.text
            # Basic HTML stripping could be added here
            self.data.append(text)
            return text
        except Exception as e:
            print(f"Error loading URL {url}: {e}")
            return ""

    def load_from_string(self, text):
        self.data.append(text)

    def prepare_data(self, sequence_length=5):
        # Prepare X, Y for next-word prediction
        full_text = " ".join(self.data)
        self.tokenizer.fit_on_text(full_text)
        sequences = self.tokenizer.texts_to_sequences([full_text])[0]
        
        X = []
        Y = []
        for i in range(len(sequences) - sequence_length):
            X.append(sequences[i:i+sequence_length])
            Y.append(sequences[i+sequence_length])
            
        return X, Y
