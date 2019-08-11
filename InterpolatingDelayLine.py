import numpy as np

class InterpolatingDelayLine:
    def __init__(self, max_delay_length_samples=44100):
        self.delay_line = np.zeros(max_delay_length_samples)

        self.read_sample = 0
        self.write_sample = 0
        self.set_delay_samples(max_delay_length_samples)
        

    def set_delay_samples(self, delay_length_samples):
        self.read_sample = self.write_sample - delay_length_samples
        while self.read_sample < 0:
            self.read_sample += self.delay_line.size

    def get(self):
        return self.get_tap(0)

    def get_tap(self, tap_samples):
        read_sample_floor = int(self.read_sample + tap_samples)
        interp = self.read_sample + tap_samples - read_sample_floor
        y = interp * self.delay_line[read_sample_floor % self.delay_line.size]
        y += (1 - interp) * self.delay_line[(read_sample_floor + 1) % self.delay_line.size]
        return y

    def get_all(self):
        return self.delay_line

    def set_all(self, contents):
        self.delay_line[:len(contents)] = contents
        self.read_sample = 0
        self.write_sample = 0
        self.set_delay_samples(self.delay_line.size)

    def tick(self, x):
        self.delay_line[self.write_sample] = x
        y = self.get()

        self.write_sample += 1
        self.read_sample += 1
        if self.write_sample >= self.delay_line.size:
            self.write_sample -= self.delay_line.size
        if self.read_sample >= self.delay_line.size:
            self.read_sample -= self.delay_line.size

        return y


    # convenience function to tick through many samples
    def tick_all(self, samples):
        return [self.tick(x) for x in samples]

    def clear(self):
        self.set_all(np.zeros(self.delay_line.size))
