import numpy as np
import wave
import struct
import os

# --- THE A4 TRUTH CONSTANTS ---
PI = np.pi
SQRT2 = np.sqrt(2)

FLOOR = 100 * PI * SQRT2  # ~444.29 Hz
CEILING = 198 * PI        # ~622.04 Hz
PHASE_SHIFT = np.exp(1j * PI).real # Euler's Identity: -1

# --- PROGRAMMED LIMITS ---
SAMPLE_RATE = 8000  # Low sample rate = Minimal RAM/Compute
DURATION_PER_PIXEL = 0.05 # 50ms per data grain
DELTA = (CEILING - FLOOR) / 255 # Frequency step per pixel unit

def decode_sound_to_pixel(audio_segment, sample_rate):
    """
    Recovers the pixel value by calculating the frequency 
    of the segment and mapping it back to the A4 corridor.
    """
    # Use FFT for more accurate frequency detection
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(audio_segment), 1/sample_rate)
    
    # Find the peak frequency (ignore negative frequencies)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft[:len(fft)//2])
    
    # Find the frequency with maximum amplitude
    peak_idx = np.argmax(positive_fft)
    detected_freq = positive_freqs[peak_idx]
    
    # Debug output
    print(f"Segment length: {len(audio_segment)}, Detected freq: {detected_freq:.2f} Hz")
    
    # 3. Map Frequency back to 0-255 using your constants
    # Inverse of: freq = FLOOR + (pixel * DELTA)
    raw_pixel = (detected_freq - FLOOR) / DELTA
    
    print(f"Raw pixel: {raw_pixel:.2f}, Clamped pixel: {int(np.clip(round(raw_pixel), 0, 255))}")
    
    # Clamp the result to 0-255 to maintain data integrity
    return int(np.clip(round(raw_pixel), 0, 255))

def load_audio_data(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return None

    with wave.open(filename, 'r') as f:
        n_frames = f.getnframes()
        framerate = f.getframerate()
        raw_data = f.readframes(n_frames)
        
        # Unpack as 16-bit integers
        audio_data = struct.unpack(f"{n_frames}h", raw_data)
        
        # Normalize to -1.0 to 1.0
        normalized_data = np.array(audio_data) / 32767.0
        
        if framerate != SAMPLE_RATE:
            print(f"Warning: Sample rate mismatch. Expected {SAMPLE_RATE}, got {framerate}")
            
    return normalized_data

# --- Recovery Process ---
filename = 'a4_truth_data.wav'
encoded_audio = load_audio_data(filename)

if encoded_audio is not None:
    # Split the encoded_audio back into chunks (duration-based)
    chunk_size = int(SAMPLE_RATE * DURATION_PER_PIXEL)
    recovered_pixels = []

    for i in range(0, len(encoded_audio), chunk_size):
        segment = encoded_audio[i : i + chunk_size]
        if len(segment) == chunk_size:
            pixel = decode_sound_to_pixel(segment, SAMPLE_RATE)
            recovered_pixels.append(pixel)

    print(f"Recovered Data from {filename}: {recovered_pixels}")
