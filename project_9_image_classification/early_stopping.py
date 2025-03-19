# early_stopping.py
class EarlyStopping:
    def __init__(self, patience=10, mode="max", delta=0.005):
        self.patience = patience
        self.mode = mode
        self.delta = delta
        self.best_score = None
        self.counter = 0
        self.early_stop = False

    def __call__(self, current_score):
        if self.best_score is None:
            self.best_score = current_score
        elif (self.mode == "max" and current_score < self.best_score + self.delta) or (
            self.mode == "min" and current_score > self.best_score - self.delta
        ):
            self.counter += 1
            print(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = current_score
            self.counter = 0
