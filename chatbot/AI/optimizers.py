class SGD:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate
    
    def update(self, layer, grad):
        # In our implementation, Layer.backward handles the update directly for simplicity.
        # So optimizer just holds the rate.
        pass
