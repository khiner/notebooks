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
        for i in range(self.b.size - 1, 0, -1):
            self.outputs[0] += self.b[i] * self.inputs[i]
            self.inputs[i] = self.inputs[i-1]

        self.outputs[0] += self.b[0] * self.inputs[0]

        for i in range(self.a.size - 1, 0, -1):
            self.outputs[0] += -self.a[i] * self.outputs[i]
            self.outputs[i] = self.outputs[i-1]

        return self.outputs[0]
    
    # Convenience method wrapping around scipy.signal.freqz
    def freqz(self):
        return freqz(self.b, self.a)


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

    def clear(self):
        self.in1 = 0.0
        self.in2 = 0.0

class PoleZeroFilter():
    def __init__(self):
        self.set_coefficients()
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
