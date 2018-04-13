import numpy as np

from conversion import SAMPLES_PER_SECOND

MAX_NOTE_DURATION_SECONDS = 20
MAX_NOTE_DURATION_SAMPLES = MAX_NOTE_DURATION_SECONDS * SAMPLES_PER_SECOND
# share this 0:MAX_N range
TIME_RANGE = np.linspace(0, MAX_NOTE_DURATION_SECONDS, SAMPLES_PER_SECOND * MAX_NOTE_DURATION_SECONDS)

def generate_sine(frequency, duration_samples):
    if duration_samples > MAX_NOTE_DURATION_SAMPLES:
        print('Clipping note length from %f seconds to %f seconds.' % duration_samples / SAMPLES_PER_SECOND, MAX_NOTE_DURATION_SECONDS)
        duration_samples = MAX_NOTE_DURATION_SAMPLES
    return np.sin(2 * np.pi * frequency * TIME_RANGE[:duration_samples])


def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

# I think this is whack...
# Looking up "power spectral density", I think this is not going to give the right power value for band-limited white noise...?
# Should be close anyway.
def total_power(samples):
    return np.sqrt(np.var(samples) * len(samples))

def band_limited_noise(min_freq, max_freq, num_samples=SAMPLES_PER_SECOND):
    freqs = np.abs(np.fft.fftfreq(num_samples, 1 / SAMPLES_PER_SECOND))
    f = np.zeros(num_samples)
    f[np.where(np.logical_and(freqs >= min_freq, freqs <= max_freq))[0]] = 1
    bln = fftnoise(f)
    return bln / total_power(bln) # normalize to total power of 1
