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

def zplane(zeros, poles, ax=None, zeros_ax=None, poles_ax=None):
    """Plot the complex z-plane given zeros and poles."""

    zeros = np.asarray(zeros).astype(complex)
    poles = np.asarray(poles).astype(complex)

    if ax is None:    
        ax = plt.subplot(111)

    if zeros_ax is None and poles_ax is None:
        ax.add_patch(patches.Circle((0,0), radius=1, fill=False, color='black', ls='solid', alpha=0.2))
        ax.axvline(0, color='0.7'); ax.axhline(0, color='0.7')

    if poles.size > 0:
        if poles_ax is None:
            poles_ax, = ax.plot(poles.real, poles.imag,  'x', markersize=9, label='poles')
        else:
            poles_ax.set_data(poles.real, poles.imag)

    if zeros.size > 0:
        if zeros_ax is None:
            zeros_ax, = ax.plot(zeros.real, zeros.imag, 'o', markersize=9, fillstyle='none', label='zeros')
        else:
            zeros_ax.set_data(zeros.real, zeros.imag)
    ax.legend()

    ax.set_aspect('equal')
    return zeros_ax, poles_ax
