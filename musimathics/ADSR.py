import numpy as np

from constants import SAMPLES_PER_SECOND

class ADSR:
    # freq of 0 is interpreted as rest
    def __init__(self, attack_seconds=0.1, decay_seconds=0.1, sustain_level=0.8, release_seconds=0.01):
        self.set(attack_seconds, decay_seconds, sustain_level, release_seconds)

    # uses simple linear ramps
    def set(self, attack_seconds, decay_seconds, sustain_level, release_seconds):
        self.attack_samples = int(attack_seconds * SAMPLES_PER_SECOND)
        self.decay_samples = int(decay_seconds * SAMPLES_PER_SECOND)
        self.sustain_level = sustain_level
        self.release_samples = int(release_seconds * SAMPLES_PER_SECOND)

    def apply(self, samples):
        samples[:self.attack_samples] *= np.linspace(0, 1, self.attack_samples)
        samples[self.attack_samples:(self.attack_samples + self.decay_samples)] *= np.linspace(1, self.sustain_level, self.decay_samples)
        samples[(self.attack_samples + self.decay_samples):-self.release_samples] *= self.sustain_level
        samples[-self.release_samples:] *= np.linspace(self.sustain_level, 0, self.release_samples)
