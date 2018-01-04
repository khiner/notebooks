# Simple, unoptomized DFT/IDFT function implementations

import numpy as np
from scipy import signal

def DFT(x):
    """
    Unoptimized, straight-agead version of DFT
    Input:
        x (numpy array) = input sequence of length N
    Output:
        X (numpy array) = The N point DFT of the input sequence x
    """
    N = x.size
    xn = np.arange(N)
    return np.array([ (x * np.exp(-1j * 2 * np.pi * k / N * xn)).sum() for k in xn ])

def IDFT(X):
    """
    Unoptimized, straight-agead version of inverst DFT
    Input:
        X (numpy array) = frequency spectrum (length N)
    Output:
        x (numpy array) = The N point IDFT of the frequency spectrum X
    """
    N = X.size
    xn = np.arange(N)
    return np.array([ 1.0 / N * (X * np.exp(1j * 2 * np.pi * n / N * xn)).sum() for n in xn ])

# Take only positive frequency components of a spectrum
# !Assumes X is the direct result of a DFT on a real signal (with negative frequencies included)
def get_positive_frequencies(X):
    return X[:X.size // 2]

def get_magnitude_and_phase(x):
    """    
    Returns mX, pX: the absolute value of the positive frequencies of the DFT of the given real signal and the phase values
    """
    X = get_positive_frequencies(np.fft.fft(x))
    mX = np.abs(X)
    pX = np.unwrap(np.angle(X)) # unwrapped phase spectrum of positive frequencies
    return mX, pX

def detect_peaks(mX, t):
    """
    Detect spectral peak locations
    mX: magnitude spectrum, t: threshold
    returns ploc: peak locations
    """

    thresh = np.where(mX[1:-1] > t, mX[1:-1], 0);           # locations above threshold
    next_minor = np.where(mX[1:-1] > mX[2:], mX[1:-1], 0)   # locations higher than the next one
    prev_minor = np.where(mX[1:-1] > mX[:-2], mX[1:-1], 0)  # locations higher than the previous one
    peak_locations = thresh * next_minor * prev_minor       # locations fulfilling the three criteria
    peak_locations = peak_locations.nonzero()[0] + 1        # add 1 to compensate for previous steps
    return peak_locations

def interpolate_parabolic(mX, pX, peak_locations):
    """
    Interpolate peak values using parabolic interpolation
    mX, pX: magnitude and phase spectrum, ploc: locations of peaks
    returns iploc, ipmag, ipphase: interpolated peak location, magnitude and phase values
    """

    val = mX[peak_locations]                                                # magnitude of peak bin
    lval = mX[peak_locations - 1]                                           # magnitude of bin at left
    rval = mX[peak_locations + 1]                                           # magnitude of bin at right
    ip_loc = peak_locations + 0.5 * (lval - rval) / (lval - 2 * val + rval) # center of parabola
    ip_mag = val - 0.25 * (lval - rval) * (ip_loc - peak_locations)         # magnitude of peaks
    ip_phase = np.interp(ip_loc, np.arange(0, pX.size), pX)                 # phase of peaks by linear interpolation
    return ip_loc, ip_mag, ip_phase

def dft_model(x, N, w):
    """
    Applies the given window (unless given window is None)
    Applies zero-phase-windowing
    Returns the magnitude spectrum and phase values
    """
    M = x.size
    xw = x * (w / sum(w)) if w is not None else x
    hM1 = (M + 1) // 2 # half analysis window
    hM2 = M // 2 # half analysis window size by floor
    zero_phase_windowed_xw = np.zeros(N)
    zero_phase_windowed_xw[:hM1] = xw[hM2:]
    zero_phase_windowed_xw[-hM2:] = xw[:hM2]
    return get_magnitude_and_phase(zero_phase_windowed_xw)

def sinc(x, N):
    """
    Generate the main lobe of a sinc function (Dirichlet kernel)
    x: array of indexes to compute; N: size of FFT to simulate
    returns y: samples of the main lobe of a sinc function
    """
    y = np.sin(N * x / 2) / np.sin(x / 2) # compute the sinc function
    y[np.isnan(y)] = N                    # avoid NaN if x == 0
    return y

def gen_bh_lobe(x):
    """
    Generate the main lobe of a Blackman-Harris window
    x: bin positions to compute (real values)
    returns y: main lobe os spectrum of a Blackman-Harris window
    """

    N = 512                                                 # size of fft to use
    f = x * np.pi * 2 / N                                   # frequency sampling
    df = 2 * np.pi / N
    y = np.zeros(x.size)                                    # initialize window
    consts = [0.35875, 0.48829, 0.14128, 0.01168]           # window constants
    for m in range(0, 4):                                   # iterate over the four sincs to sum
        y += consts[m] / 2 * (sinc(f - df * m, N) + sinc(f + df * m, N))  # sum of scaled sinc functions
    return y / N / consts[0] # normalize

def gen_spec_sines(ip_freq, ip_mag, ip_phase, N, fs):
    """
    Generate a spectrum from a series of sine values
    ip_freq, ip_mag, ip_phase: sine peaks locations, magnitudes and phases
    N: size of the complex spectrum to generate; fs: sampling rate
    returns Y: generated complex spectrum of sines
    """

    Y = np.zeros(N, dtype = np.complex_)             # initialize output complex spectrum
    hN = int(N / 2)                                       # size of positive freq. spectrum
    for i in range(0, ip_freq.size):                 # generate all sine spectral lobes
        loc = N * ip_freq[i] / fs                    # it should be in range ]0,hN-1[
        if loc == 0 or loc > hN - 1: continue
        bin_remainder = round(loc) - loc
        lb = np.arange(bin_remainder - 4, bin_remainder + 5) # main lobe (real value) bins to read
        lmag = gen_bh_lobe(lb) * ip_mag[i]                   # lobe magnitudes of the complex exponential
        b = np.arange(round(loc) - 4, round(loc) + 5)
        for m in range(0, 9):
            bm = int(b[m])
            if bm < 0:                                 # peak lobe crosses DC bin
                Y[-bm] += lmag[m] * np.exp(-1j * ip_phase[i])
            elif bm > hN:                              # peak lobe croses Nyquist bin
                Y[bm] += lmag[m] * np.exp(-1j * ip_phase[i])
            elif bm == 0 or b[m] == hN:                # peak lobe in the limits of the spectrum
                Y[bm] += lmag[m] * np.exp(1j * ip_phase[i]) + lmag[m] * np.exp(-1j * ip_phase[i])
            else:                                        # peak lobe in positive freq. range
                Y[bm] += lmag[m] * np.exp(1j * ip_phase[i])
        Y[hN + 1:] = Y[hN - 1:0:-1].conjugate()          # fill the negative part of the spectrum
    return Y
