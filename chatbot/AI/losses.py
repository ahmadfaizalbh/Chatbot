from chatbot.AI.engine import PyMatrix

class MSE:
    def forward(self, y_pred, y_true):
        # MSE = mean((y_pred - y_true)^2)
        diff = y_pred.sub(y_true)
        # Square is manually multiplying by self
        sq = diff.mul(diff)
        
        # Mean
        total_sum = 0
        data = sq.to_list()
        count = 0
        for row in data:
            for val in row:
                total_sum += val
                count += 1
        return total_sum / count

    def backward(self, y_pred, y_true):
        # dMSE/dPred = 2/N * (y_pred - y_true)
        diff = y_pred.sub(y_true)
        n = y_pred.rows * y_pred.cols
        return diff.scale(2.0 / n)
