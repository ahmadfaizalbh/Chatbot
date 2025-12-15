from chatbot.AI.engine import PyMatrix

class Sequential:
    def __init__(self, layers=None):
        self.layers = layers if layers else []

    def add(self, layer):
        self.layers.append(layer)

    def predict(self, input_data):
        # Forward pass through all layers
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def backward(self, output_gradient, learning_rate):
        # Backward pass
        grad = output_gradient
        for layer in reversed(self.layers):
            grad = layer.backward(grad, learning_rate)
