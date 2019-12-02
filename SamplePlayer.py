class SamplePlayer:
    def __init__(self, samples):
        self.samples = samples
        self.sample_index = 0

    def tick(self):
        if self.is_finished():
            return 0.0

        out_sample = self.samples[self.sample_index]
        self.sample_index += 1

        return out_sample

    def reset(self):
        self.sample_index = 0

    def is_finished(self):
        return self.sample_index >= len(self.samples)

import numpy as np
from scipy.io.wavfile import read as read_wav

class WavPlayer(SamplePlayer):
    def __init__(self, wav_file_path):
        self.fs, samples = read_wav(wav_file_path)
        super(WavPlayer, self).__init__(samples if np.isscalar(samples[0]) else samples[:,0])
