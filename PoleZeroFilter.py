class PoleZeroFilter():
    def __init__(self):
        self.set_coefficients()
        self.out_1 = 0.0
        self.in_1 = 0.0
    
    def tick(self, in_sample):
        out_sample = self.b_0 * in_sample + self.b_1 * self.in_1 - self.a_1 * self.out_1
        self.in_1 = in_sample
        self.out_1 = out_sample
        
        return out_sample
    
    def set_coefficients(self, b_0=1.0, b_1=0.0, a_1=1.0):
        self.b_0 = b_0
        self.b_1 = b_1
        self.a_1 = a_1
