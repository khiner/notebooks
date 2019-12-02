# This class implements a fractional-length digital delay-line using
# a first-order allpass filter.  If the delay and maximum length are
# not specified during instantiation, a fixed maximum length of 4095
# and a delay of 0.5 is set.

# An allpass filter has unity magnitude gain but variable phase
# delay properties, making it useful in achieving fractional delays
# without affecting a signal's frequency magnitude response.  In
# order to achieve a maximally flat phase delay response, the
# minimum delay possible in this implementation is limited to a
# value of 0.5.

import numpy as np

class AllpassDelay:
    def __init__(self, delay_samples, max_delay_samples):
        self.max_delay_samples = max_delay_samples
        # Writing before reading allows delays from 0 to length-1. 
        self.inputs = np.zeros(max_delay_samples + 1)
        self.last_out = 0.0
        self.next_out = 0.0
        self.in_pointer = 0
        self.set_delay_samples(delay_samples)
        self.allpass_input = 0.0
        self.do_next_out = True

    def tick(self, in_sample=0.0):
        self.inputs[self.in_pointer] = in_sample
        self.in_pointer += 1
        if self.in_pointer == self.inputs.size:
            self.in_pointer = 0

        self.last_out = self.get_next_out()
        self.do_next_out = True

        self.allpass_input = self.inputs[self.out_pointer]
        self.out_pointer += 1
        if self.out_pointer == self.inputs.size:
            self.out_pointer = 0

        return self.last_out

    def get_next_out(self):
        if self.do_next_out:
            self.next_out = -self.allpass_coefficient * self.last_out
            self.next_out += self.allpass_input + (self.allpass_coefficient * self.inputs[self.out_pointer])
            self.do_next_out = False

        return self.next_out

    def set_max_delay_samples(self, max_delay_samples):
        if max_delay_samples >= self.inputs.size:
            self.inputs = np.concatenate([self.inputs, np.zeros(max_delay_samples + 1)])

    def set_delay_samples(self, delay_samples):
        assert(delay_samples >= 0.5)
        assert(delay_samples <= self.max_delay_samples)

        self.delay_samples = delay_samples

        fractional_out_pointer = self.in_pointer - self.delay_samples + 1.0 # out_pointer chases in_pointer
        while fractional_out_pointer < 0:
            fractional_out_pointer += self.inputs.size
        self.out_pointer = int(fractional_out_pointer)
        if self.out_pointer == self.inputs.size:
            self.out_pointer = 0
        self.alpha = 1.0 + self.out_pointer - fractional_out_pointer # fractional part

        if self.alpha < 0.5:
            # The optimal range for alpha is about 0.5 - 1.5 in order to
            # achieve the flattest phase delay response.
            self.out_pointer += 1
            if self.out_pointer >= self.inputs.size:
                self.out_pointer -= self.inputs.size
            self.alpha += 1.0

        self.allpass_coefficient = (1.0 - self.alpha) / (1.0 + self.alpha)

    def clear(self):
        self.inputs[:] = 0.0
        self.allpass_input = 0.0

    def tap_out(self, tap_delay):
        tap = int(self.in_pointer - tap_delay - 1)
        while tap < 0:
            tap += self.inputs.size
        return self.inputs[tap]

    def tap_in(self, value, tap_delay):
        tap = int(self.in_pointer - tap_delay - 1)
        while tap < 0:
            tap += self.inputs.size
        self.inputs[tap] = value
