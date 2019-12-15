import numpy as np
from matplotlib import pyplot as plt


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
            phase = phase / max(w, 1e-12) #prevent div by zero
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
