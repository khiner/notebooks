import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

def plot_frequency_response(X, f=None):
    """
    X: frequency response
    f: vector of corresponding frequency values
    """

    Xm = np.abs(X)
    Xmdb = 20 * np.log10(Xm)
    Xp = np.angle(X)

    if f is None:
        N = len(X)
        f = np.arange(N) / (2 * (N - 1))

    plt.subplot(211)
    plt.plot(f, Xmdb, '-k')
    plt.grid(True)
    plt.ylabel('Gain (dB)')
    plt.xlabel('Normalized Frequency (cycles/sample)')
    plt.autoscale(enable=True, axis='x', tight=True)

    plt.subplot(212)
    plt.plot(f, Xp, '-k')
    plt.grid(True)
    plt.ylabel('Phase Shift (radians)')
    plt.xlabel('Normalized Frequency (cycles/sample)')
    plt.autoscale(enable=True, axis='x', tight=True)

    plt.tight_layout()

    return plt

def zplane(zeros, poles):
    """Plot the complex z-plane given zeros and poles."""
    
    ax = plt.subplot(111)

    ax.add_patch(patches.Circle((0,0), radius=1, fill=False, color='black', ls='solid', alpha=0.2))
    plt.axvline(0, color='0.7'); plt.axhline(0, color='0.7')
    
    plt.plot(poles.real, poles.imag, 'x', markersize=9, label='poles')
    plt.plot(zeros.real, zeros.imag,  'o', markersize=9, fillstyle='none', label='zeros')
    plt.legend()
