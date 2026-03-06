import numpy as np
import wave
import struct

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

def encode_pixel_to_sound(pixel_value):
    """
    Converts a single pixel (0-255) into a resonant frequency 
    within the A4 Truth corridor.
    """
    # Calculate the specific frequency for this piece of data
    freq = FLOOR + (pixel_value * DELTA)
    
    t = np.linspace(0, DURATION_PER_PIXEL, int(SAMPLE_RATE * DURATION_PER_PIXEL))
    
    # Generate the wave: The 'Math Truth' in motion
    # We multiply by PHASE_SHIFT (-1) at the tail to 'close' the data packet
    wave_data = np.sin(2 * PI * freq * t)
    
    return wave_data

def process_image_data(pixels):
    audio_buffer = []
    for p in pixels:
        audio_buffer.append(encode_pixel_to_sound(p))
    return np.concatenate(audio_buffer)

# Example: Encoding a more comprehensive test 'Image' 
example_data = [0, 32, 64, 96, 128, 160, 192, 224, 255]
encoded_audio = process_image_data(example_data)

# Save to a minimal WAV file
with wave.open('a4_truth_data.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    for sample in encoded_audio:
        f.writeframes(struct.pack('h', int(sample * 32767)))

print("Data encoded into 'a4_truth_data.wav' using minimal compute.")
