import numpy as np

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
    def __init__(self, gain=1.0):
        self.gain = gain

    def tick(self):
        return self.gain * np.random.uniform(low=-1.0, high=1.0)

    def reset(self):
        return self

# Very naive implementation
class SineGenerator:
    def __init__(self, fs=44100):
        self.fs = fs
        self.frequency = 1.0
        self.amplitude = 1.0
        self.t_radians = 0.0

    def tick(self):
        out_sample = self.amplitude * np.sin(self.t_radians)
        self.t_radians += 2 * np.pi * self.frequency / self.fs
        return out_sample

    def set_frequency(self, frequency):
        self.frequency = frequency
