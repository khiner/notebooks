import numpy as np

from conversion import SAMPLES_PER_SECOND
from generators import generate_sine
from ADSR import ADSR

class Note:
    # freq of 0 is interpreted as rest
    def __init__(self, frequency=880, duration_seconds=0.5, level=0.8, pan=0.5, attack_seconds=0.1, decay_seconds=0.1, sustain_level=0.8, release_seconds=0.01):
        self.frequency = frequency
        self.level = level
        self.pan = pan
        self.duration_samples = int(duration_seconds * SAMPLES_PER_SECOND)
        if attack_seconds + decay_seconds >= duration_seconds:
            remainder = attack_seconds + decay_seconds - duration_seconds
            attack_seconds -= remainder / 2
            decay_seconds -= remainder / 2
        self.set_adsr(ADSR(attack_seconds, decay_seconds, sustain_level, release_seconds))

    def set_adsr(self, adsr):
        self.adsr = adsr
        self.__update_samples()

    def get_samples(self):
        return self.samples

    def __update_samples(self):
        if self.frequency == 0:
            self.samples = np.zeros(self.duration_samples + self.adsr.release_samples)
        else:
            self.samples = generate_sine(self.frequency, self.duration_samples + self.adsr.release_samples)
            self.adsr.apply(self.samples)
            self.samples *= self.level
