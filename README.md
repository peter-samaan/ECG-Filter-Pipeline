# ECG Filter Pipeline

## Overview
This project implements a full ECG signal processing pipeline to clean and analyze heart signal data. The goal was to remove noise from raw ECG recordings and accurately detect heartbeats to compute heart rate.

## Dataset
- MIT-BIH Arrhythmia Database

## Features
- Noise reduction using digital filtering
- Frequency-domain analysis using FFT
- R-peak detection for heartbeat identification
- Heart rate calculation from detected peaks

## Methods

### 1. Signal Preprocessing
Raw ECG signals contain noise such as:
- Baseline drift
- Powerline interference (60 Hz)

To address this, I designed:
- Butterworth bandpass filter
- 60 Hz notch filter

### 2. Frequency Analysis
- Applied Fast Fourier Transform (FFT)
- Verified removal of unwanted frequency components
- Compared signals before and after filtering

### 3. R-Peak Detection
- Implemented an algorithm to detect R-peaks
- Extracted heartbeat intervals
- Computed heart rate from peak timing

## Results
- Successfully removed baseline drift and 60 Hz noise
- Clear ECG waveform after filtering
- Accurate detection of R-peaks
- Reliable heart rate estimation

## Tools & Technologies
- Python
- NumPy
- SciPy

## Future Improvements
- Improve peak detection robustness
- Add real-time processing
- Test on additional datasets
