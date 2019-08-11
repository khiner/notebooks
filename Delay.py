import numpy as np

class Delay:
    def __init__(self, max_delay_length_samples=44100):
        self.delay_line = np.zeros(max_delay_length_samples)

        self.read_sample = 0
        self.write_sample = 0
        self.wet_amount = 0.5
        self.delay_growth_samples = 0

    def set_delay_samples(self, delay_length_samples):
        self.read_sample = self.write_sample - delay_length_samples
        while self.read_sample < 0:
            self.read_sample += self.delay_line.size
        return True

    def set_wet_amount(self, wet_amount):
        self.wet_amount = wet_amount

    def set_delay_growth_samples(self, delay_growth_samples):
        self.delay_growth_samples = delay_growth_samples

    def tick(self, x):
        self.delay_line[self.write_sample] = x
        read_sample_floor = int(self.read_sample)
        interp = self.read_sample - read_sample_floor
        y = interp * self.delay_line[read_sample_floor]
        y += (1 - interp) * self.delay_line[(read_sample_floor + 1) % self.delay_line.size]

        self.write_sample += 1
        self.read_sample += 1 - self.delay_growth_samples
        if self.write_sample >= self.delay_line.size:
            self.write_sample -= self.delay_line.size
        if self.read_sample >= self.delay_line.size:
            self.read_sample -= self.delay_line.size
        elif self.read_sample < 0:
            self.read_sample += self.delay_line.size

        return x * (1 - self.wet_amount) + y * self.wet_amount
    
    # convenience function to tick through many samples
    def tick_all(self, samples):
        return [self.tick(x) for x in samples]
