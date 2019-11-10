from scipy.io.wavfile import read as read_wav

class WavPlayer:
    def __init__(self, wav_file_path):
        self.fs, self.samples = read_wav(wav_file_path)
        self.samples = self.samples[:, 0] # take left channel as mono
        self.samples = self.samples / self.samples.max()
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
