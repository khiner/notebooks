import numpy as np

from conversion import SAMPLES_PER_SECOND

class AR:
    # freq of 0 is interpreted as rest
    def __init__(self, attack_seconds=0.1, release_seconds=0.1):
        self.set(attack_seconds, release_seconds)

    # uses simple linear ramps
    def set(self, attack_seconds, release_seconds):
        self.attack_samples = int(attack_seconds * SAMPLES_PER_SECOND)
        self.release_samples = int(release_seconds * SAMPLES_PER_SECOND)

    def apply(self, samples):
        return self.apply_linear(samples)

    def apply_linear(self, samples):
        samples[:self.attack_samples] *= np.linspace(0, 1, self.attack_samples)
        samples[-self.release_samples:] *= np.linspace(1, 0, self.release_samples)

        return samples # chain

    # not implemented
    def apply_exponential(self, samples):
        return self.apply_linear(samples)
