class ImpulseGenerator:
    def __init__(self):
        self.is_first_sample = True
    
    def tick(self):
        out = 1.0 if self.is_first_sample else 0.0
        self.is_first_sample = False
        return out
    
    def reset(self):
        self.is_first_sample = True

class NoiseGenerator:
    def tick(self):
        return np.random.uniform(low=-1.0, high=1.0)

    def reset(self):
        return self
