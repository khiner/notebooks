import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
np.seterr(divide='ignore', invalid='ignore')

def plot_frequency_response(w, H, fig=None, frequency_plot=None, phase_plot=None, db=True,
                            lower_db_lim=None, upper_db_lim=None, show_phase_plot=True,
                            unwrap_phase=True, phase_delay=False):
    if not fig and not frequency_plot and not phase_plot:
        if show_phase_plot:
            fig, [frequency_plot, phase_plot] = plt.subplots(2, 1, figsize=(10, 6))
        else:
            fig, frequency_plot = plt.subplots(1, 1, figsize=(10, 3))

    frequency_plot.plot(w, 20*np.log10(np.abs(H)) if db else np.abs(H), c='r', linewidth=2)
    frequency_plot.grid(True)
    frequency_plot.set_title('Magnitude Response', size=16)
    frequency_plot.set_ylabel('Gain (dB)' if db else 'Gain')
    frequency_label = 'Frequency (radians/sample)'
    frequency_plot.set_xlabel(frequency_label)
    if db and (lower_db_lim or upper_db_lim):
        frequency_plot.set_ylim(lower_db_lim or -100, upper_db_lim or 1)
    elif not db:
        frequency_plot.set_ylim(0, 1.1)
    frequency_plot.autoscale(enable=True, axis='x', tight=True)

    if show_phase_plot:
        phase = np.angle(H)
        if unwrap_phase:
            phase = np.unwrap(phase)
        if phase_delay:
            phase = phase / w
        phase_plot.plot(w, phase, c='g', linewidth=2)
        phase_plot.grid(True)
        phase_plot.set_title('Phase Response', size=16)
        frequency_units = 'samples' if phase_delay else 'radians' 
        phase_plot.set_ylabel('Phase (%s)' % frequency_units)
        phase_plot.set_xlabel(frequency_label)
        if phase.min() >= -np.pi and phase.max() <= np.pi:
            phase_plot.set_yticks(np.pi * np.array([-1, -1/2, 0, 1/2, 1]))
            phase_plot.set_yticklabels(['$-\\pi$', '$-\\dfrac{\\pi}{2}$', '$0$', '$\\dfrac{\\pi}{2}$', '$\\pi$'])
        phase_plot.autoscale(enable=True, axis='x', tight=True)

    plt.tight_layout()

    return fig, [frequency_plot, phase_plot]


def zplane(zeros, poles, fig=None, ax=None, zeros_ax=None, poles_ax=None):
    """Plot the complex z-plane given zeros and poles."""

    zeros = np.asarray(zeros).astype(complex)
    poles = np.asarray(poles).astype(complex)

    if fig is None:
        plt.figure(figsize=(8, 8))

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
