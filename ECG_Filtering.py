import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wfdb

fs = 500 # Sampling frequency
f0 = 60 # Interference frequency
fl = 0.5 # HPF cutoff frequency
fh = 100 # LPF cutoff frequency
'''
# Generate a sample ECG signal (for demonstration purposes)
t = np.arange(0, 5, 1/fs)
ecg_clean = np.sin(2*np.pi*1*t) + 0.5*np.sin(2*np.pi*3*t)
noise = 0.3*np.sin(2*np.pi*60*t)
ecg_noisy = ecg_clean + noise
'''
# Load real ECG signal
record = wfdb.rdrecord('100', pn_dir='mitdb')
ecg_noisy = record.p_signal[:, 0]
fs = record.fs
t = np.arange(len(ecg_noisy)) / fs

# Notch filter
b1, a1 = signal.iirnotch(f0, Q=30, fs=fs)

# HPF
b2, a2 = signal.butter(4, fl, btype="high", fs=fs, analog=False)

# LPF
b3, a3 = signal.butter(4, fh, btype="low", fs=fs, analog=False)

# Apply filters
ecg_notched = signal.filtfilt(b1, a1, ecg_noisy)
ecg_highpassed = signal.filtfilt(b2, a2, ecg_notched)
ecg_filtered = signal.filtfilt(b3, a3, ecg_highpassed)

# Detect R-peaks
threshold = np.mean(ecg_filtered) + 0.5*np.std(ecg_filtered)
peaks, properties = signal.find_peaks(
    ecg_filtered,
    distance = 0.4*fs, # Minimum distance between peaks (0.4 seconds)
    height = threshold # Ignore small peaks
)

# frequency response of the filter
b = np.convolve(b1, np.convolve(b2, b3))
a = np.convolve(a1, np.convolve(a2, a3))
w, h = signal.freqz(b, a, fs=fs)

# I/O Signals
N = len(ecg_noisy)
freqs = np.fft.fftfreq(N, 1/fs)
Xn = np.fft.fft(ecg_noisy)
Yn = np.fft.fft(ecg_filtered)

# Plotting ECG before/after filtering
plt.figure()
plt.plot(t, ecg_noisy, label='Noisy ECG')
plt.plot(t, ecg_filtered, label='Filtered ECG')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Plotting Filtered ECG with detected R-peaks
plt.figure()
plt.plot(t, ecg_filtered, label='Filtered ECG')
plt.plot(t[peaks], ecg_filtered[peaks], 'ro', label='R-peaks')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.xlim(0, 10)
plt.legend()
plt.show()

# Plotting I/O signals in frequency domain
plt.figure()
plt.plot(freqs, 20*np.log10(abs(Xn)), label="Noisy ECG")
plt.plot(freqs, 20*np.log10(abs(Yn)), label="Filtered ECG")
plt.title("Fourier :)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.xlim(-5, 200)
plt.legend()
plt.show()

# Plotting frequency response
plt.figure()
plt.plot(w, 20*np.log10(abs(h)))
plt.title("Magnitude Response")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.xlim(-20, 200)
plt.ylim(-30, 3)
plt.show()