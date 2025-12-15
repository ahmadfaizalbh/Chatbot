from chatbot.AI.engine import PyMatrix
import math

class Layer:
    def forward(self, input_data):
        raise NotImplementedError

    def backward(self, output_gradient, learning_rate):
        raise NotImplementedError

class Dense(Layer):
    def __init__(self, input_size, output_size):
        self.weights = PyMatrix(input_size, output_size)
        self.weights.randomize(-1.0, 1.0) # Simple initialization
        # Scale weights
        self.weights = self.weights.scale(math.sqrt(2.0/input_size))
        
        self.bias = PyMatrix(1, output_size)
        self.bias.randomize(-0.1, 0.1)

    def forward(self, input_data):
        self.input = input_data
        # Y = X . W + B
        self.output = self.input.dot(self.weights)
        
        # Broadcast bias add (manual broadcast for now or just add to each row)
        # Assuming batch size 1 for online learning or explicit broadcast
        # For simplicity, let's assume input is 1xN or use a bias that expands
        # Our C add requires same shape.
        
        # Hack for bias broadcasting: extend bias to match output rows
        if self.output.rows > 1:
            # We need a proper broadcast add in C or handle it here.
            # For now, let's just loop in Python for bias addition if batch > 1
            # Or assume batch=1 which is common in "Chat.converse" online learning.
            pass
        
        # We will add bias
        # Create a full bias matrix matching output shape
        # This is inefficient but "easy to setup"
        expanded_bias = PyMatrix(self.output.rows, self.output.cols)
        # Copy bias to all rows
        # Simplification: Just support batch size 1 for now or rely on user to handle
        # But training might use batches. 
        # Let's handle batch size 1 correctly, and maybe hack batch > 1
        
        # If rows=1, direct add
        if self.output.rows == 1:
            self.output = self.output.add(self.bias)
        else:
             # Very slow python loop fallback for batch > 1
             bias_list = self.bias.to_list()[0]
             out_list = self.output.to_list()
             for r in range(self.output.rows):
                 for c in range(self.output.cols):
                     out_list[r][c] += bias_list[c]
             self.output = PyMatrix.from_list(out_list)
             
        return self.output

    def backward(self, output_gradient, learning_rate):
        # dW = X^T . dY
        input_T = self.input.transpose()
        weights_gradient = input_T.dot(output_gradient)
        
        # dB = sum(dY, axis=0)
        # For batch size 1, dB = dY
        if output_gradient.rows == 1:
            bias_gradient = output_gradient
        else:
            # Sum columns
            grad_list = output_gradient.to_list()
            bias_grad_accum = [0.0] * self.bias.cols
            for r in range(output_gradient.rows):
                for c in range(output_gradient.cols):
                    bias_grad_accum[c] += grad_list[r][c]
            bias_gradient = PyMatrix.from_list([bias_grad_accum])

        # dX = dY . W^T
        weights_T = self.weights.transpose()
        input_gradient = output_gradient.dot(weights_T)
        
        # Update parameters (SGD)
        self.weights = self.weights.sub(weights_gradient.scale(learning_rate))
        self.bias = self.bias.sub(bias_gradient.scale(learning_rate))
        
        return input_gradient

class Activation(Layer):
    def __init__(self, activation_name="sigmoid"):
        self.activation_name = activation_name

    def forward(self, input_data):
        self.input = input_data
        if self.activation_name == "sigmoid":
            self.output = self.input.apply_sigmoid()
        elif self.activation_name == "relu":
            self.output = self.input.apply_relu()
        elif self.activation_name == "tanh":
            self.output = self.input.apply_tanh()
        elif self.activation_name == "softmax":
            self.output = self.input.apply_softmax()
        return self.output

    def backward(self, output_gradient, learning_rate):
        if self.activation_name == "sigmoid":
            d_act = self.input.apply_sigmoid_derivative()
        elif self.activation_name == "relu":
            d_act = self.input.apply_relu_derivative()
        elif self.activation_name == "tanh":
            d_act = self.input.apply_tanh_derivative()
        elif self.activation_name == "softmax":
             # Simplified: Softmax usually combined with Cross Entropy
             # If separate, Jacobian is complex. 
             # For this simple lib, assuming CrossEntropy+Softmax or handled elsewhere.
             # If just passing through gradient like typical in simple libs:
             # dX = dY * (Softmax * (1 - Softmax)) ?? No.
             # Let's just return output_gradient for softmax for now (assuming it's paired with loss)
             # Or implement correctly.
             # Easier: Just support Sigmoid/ReLU/Tanh for hidden. Output handled by loss.
             return output_gradient 
            
        return output_gradient.mul(d_act)
