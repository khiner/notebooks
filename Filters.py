import numpy as np
from scipy.signal import freqz

class IirFilter:
    def __init__(self, b=[1.0], a=[1.0]):
        self.b = np.array(b)
        self.a = np.array(a)
        self.inputs = np.zeros(len(b))
        self.outputs = np.zeros(len(a))
        self.gain = 1.0

    def set_gain(self, gain):
        self.gain = gain

    def tick(self, in_sample):
        self.outputs[0] = 0.0
        self.inputs[0] = in_sample * self.gain
        for i in range(self.inputs.size - 1, 0, -1):
            if i < self.b.size: # See note in `set_b_coefficients`.
                self.outputs[0] += self.b[i] * self.inputs[i]
            self.inputs[i] = self.inputs[i-1]

        self.outputs[0] += self.b[0] * self.inputs[0]

        for i in range(self.a.size - 1, 0, -1):
            self.outputs[0] += -self.a[i] * self.outputs[i]
            self.outputs[i] = self.outputs[i-1]

        return self.outputs[0]

    def set_b_coefficients(self, b):
        # Allow growing and shrinking the b coefficients with minimal noise caused by 0s in history
        # by keeping inputs as the max length of any b coefficients that have been set.
        if len(b) > len(self.inputs):
            self.inputs = np.concatenate([self.inputs, np.zeros(len(b) - len(self.inputs))])
        self.b = np.array(b)

    # Convenience method wrapping around scipy.signal.freqz
    def freqz(self):
        return freqz(self.b, self.a)


class OneZeroFilter:
    def __init__(self, zero=-1.0):
        self.in1 = self.in2 = self.out1 = 0.0
        self.set_zero(zero)

    def tick(self, in_sample):
        self.in1 = in_sample
        self.out1 = self.b1 * self.in2 + self.b0 * self.in1
        self.in2 = self.in1

        return self.out1

    def set_zero(self, zero):
        # Normalize coefficients for unity gain
        self.b0 = 1.0 / (1.0 + zero) if zero > 0 else 1.0 / (1.0 - zero)
        self.b1 = -zero * self.b0

    # TODO could be broken
    def phase_delay(self, frequency, fs=44100):
        omega_t = 2 * np.pi * frequency / fs
        real = 0.0
        imag = 0.0
        real += self.b0 * np.cos(0)
        imag -= self.b0 * np.sin(0)
        real += self.b1 * np.cos(omega_t)
        imag += self.b1 * np.sin(omega_t)
        phase = np.arctan2(imag, real)
        phase = -phase % (2 * np.pi)
        return phase / omega_t

    def set_coefficients(self, b0, b1):
        self.b0 = b0
        self.b1 = b1

    def clear(self):
        self.in1 = self.in2 = self.out1 = 0.0

# One-pole lowpass with feedback coefficient of 0.5
class OnePoleFilter:
    def __init__(self, g=0.5, p=0.5):
        self.z_1 = 0 # memory for single pole lowpass filter at bridge
        self.g = g
        self.p = p

    def tick(self, in_sample):
        out_sample = self.g * in_sample + self.p * self.z_1
        self.z_1 = out_sample
        return out_sample

    def clear(self):
        self.z_1 = 0.0

class TwoZeroFilter:
    def __init__(self):
        self.set_coefficients()
        self.in1 = 0.0
        self.in2 = 0.0
    
    def tick(self, in_sample):
        out_sample = self.b2 * self.in2 + self.b1 * self.in1 + self.b0 * in_sample
        self.in2 = self.in1
        self.in1 = in_sample
        
        return out_sample

    def set_coefficients(self, b0=1.0, b1=0.0, b2=0.0):
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2

    def get_coefficients(self):
        return [self.b0, self.b1, self.b2]

    def clear(self):
        self.in1 = 0.0
        self.in2 = 0.0

class PoleZeroFilter():
    def __init__(self, b0=1.0, b1=0.0, a1=1.0):
        self.set_coefficients(b0, b1, a1)
        self.out1 = 0.0
        self.in1 = 0.0
    
    def tick(self, in_sample):
        out_sample = self.b0 * in_sample + self.b1 * self.in1 - self.a1 * self.out1
        self.in1 = in_sample
        self.out1 = out_sample
        
        return out_sample
    
    def set_coefficients(self, b0=1.0, b1=0.0, a1=1.0):
        self.b0 = b0
        self.b1 = b1
        self.a1 = a1

    def set_block_zero(self, pole=0.99):
        self.b0 = 1.0
        self.b1 = -1.0
        self.a1 = -pole

    def clear(self):
        self.in1 = 0.0
        self.out1 = 0.0

class NoOpFilter:
    def tick(self, in_sample):
        return in_sample
    
    def clear(self):
        return self
