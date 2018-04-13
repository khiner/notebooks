SAMPLES_PER_SECOND = 44_100

import numpy as np

def linear_to_db(amplitude):
    return 0 if amplitude < 1e-16 else 20 * np.log10(amplitude)

def db_to_linear(amplitude):
    return 10 ** (amplitude / 20)
