import numpy as np

from constants import SAMPLES_PER_SECOND
from ADSR import ADSR

MAX_NOTE_DURATION_SECONDS = 20

# share this 0:MAX_N range
TIME_RANGE = np.linspace(0, MAX_NOTE_DURATION_SECONDS, SAMPLES_PER_SECOND * MAX_NOTE_DURATION_SECONDS)

class Note:
    # freq of 0 is interpreted as rest
    def __init__(self, frequency=880, duration_seconds=0.5, level=0.8, attack_seconds=0.1, decay_seconds=0.1, sustain_level=0.8, release_seconds=0.01):
        self.frequency = frequency
        self.level = level
        self.duration_samples = int(duration_seconds * SAMPLES_PER_SECOND)
        if attack_seconds + decay_seconds >= duration_seconds:
            remainder = attack_seconds + decay_seconds - duration_seconds
            attack_seconds -= remainder / 2
            decay_seconds -= remainder / 2
        self.set_adsr(ADSR(attack_seconds, decay_seconds, sustain_level, release_seconds))

    def set_adsr(self, adsr):
        self.adsr = adsr
        self.__update_data()

    def get_data(self):
        return self.data

    def __update_data(self):
        if self.frequency == 0:
            self.data = np.zeros(self.duration_samples + self.adsr.release_samples)
        else:
            self.data = np.sin(2*np.pi*self.frequency*TIME_RANGE[:(self.duration_samples + self.adsr.release_samples)])
            self.adsr.apply(self.data)
            self.data *= self.level
