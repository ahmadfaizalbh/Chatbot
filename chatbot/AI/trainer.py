from chatbot.AI.engine import PyMatrix
from chatbot.AI.losses import MSE
import random

class Trainer:
    def __init__(self, model, optimizer, loss_fn=None):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn if loss_fn else MSE()

    def train(self, X, Y, epochs=10, batch_size=1):
        # Flatten input to list of lists if needed, or handle in loop
        # X is list of sequences (indices)
        # We need to convert indices to One-Hot or Embeddings.
        # For this "light" version, let's use One-Hot encoding corresponding to vocab size.
        # Or simpler: Input dense directly (Input layer should handle embedding?)
        # Our Dense layer expects float input.
        
        # Assumption: X[i] is a list of integers.
        # We need to convert it to a Matrix. 
        # For simplicity, let's assume input is already vector or we convert here.
        
        # Actually, let's assume specific Model structure for text.
        # If user builds model, they handle it. 
        # Here we just expect X, Y to be convertible to PyMatrix.
        
        # To make it "easy", we'll do on-the-fly one-hot if X contains ints.
        pass # Placeholder for complex logic, see OnlineTrainer for simple loop

    def fit(self, X, Y, vocab_size, epochs=5):
        print(f"Training on {len(X)} samples for {epochs} epochs...")
        for epoch in range(epochs):
            total_loss = 0
            for i in range(len(X)):
                x_seq = X[i] # e.g. [1, 5, 2]
                y_target = Y[i] # e.g. 10
                
                # Convert to One-Hot Input
                # Batch size 1, sequence length L -> Input size L * vocab_size (concatenated)
                # OR Loop through sequence (RNN).
                # Since Model is a simple Sequential of Dense/Activation, it's effectively an MLP 
                # taking fixed window size if we flatten.
                
                # Flattener One-Hot
                input_data = []
                for idx in x_seq:
                    vec = [0.0] * vocab_size
                    if idx < vocab_size:
                        vec[idx] = 1.0
                    input_data.extend(vec)
                
                # Create Matrix (1 row, N cols)
                input_mat = PyMatrix.from_list([input_data])
                
                # Target One-Hot
                target_vec = [0.0] * vocab_size
                if y_target < vocab_size:
                    target_vec[y_target] = 1.0
                target_mat = PyMatrix.from_list([target_vec])
                
                # Forward
                prediction = self.model.predict(input_mat)
                
                # Loss
                loss = self.loss_fn.forward(prediction, target_mat)
                total_loss += loss
                
                # Backward
                grad = self.loss_fn.backward(prediction, target_mat)
                self.model.backward(grad, self.optimizer.learning_rate)
                
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(X)}")

class OnlineTrainer:
    def __init__(self, model, optimizer, loss_fn=None):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn if loss_fn else MSE()

    def update(self, x_seq, y_target, vocab_size):
        # Single step update used in conversation
        input_data = []
        for idx in x_seq:
            vec = [0.0] * vocab_size
            if idx < vocab_size:
                vec[idx] = 1.0
            input_data.extend(vec)
            
        input_mat = PyMatrix.from_list([input_data])
        
        target_vec = [0.0] * vocab_size
        if y_target < vocab_size:
            target_vec[y_target] = 1.0
        target_mat = PyMatrix.from_list([target_vec])
        
        prediction = self.model.predict(input_mat)
        loss = self.loss_fn.forward(prediction, target_mat)
        
        grad = self.loss_fn.backward(prediction, target_mat)
        self.model.backward(grad, self.optimizer.learning_rate)
        return loss
