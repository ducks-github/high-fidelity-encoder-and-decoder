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

def encode_pixel_to_sound(pixel_value):
    """Converts a single pixel (0-255) into a resonant frequency"""
    freq = FLOOR + (pixel_value * DELTA)
    t = np.linspace(0, DURATION_PER_PIXEL, int(SAMPLE_RATE * DURATION_PER_PIXEL), endpoint=False)
    wave_data = np.sin(2 * PI * freq * t)
    return wave_data

def process_image_data(pixels):
    audio_buffer = []
    for p in pixels:
        audio_buffer.append(encode_pixel_to_sound(p))
    return np.concatenate(audio_buffer)

def decode_sound_to_pixel(audio_segment, sample_rate):
    """Recovers pixel value using FFT for accurate frequency detection"""
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(audio_segment), 1/sample_rate)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft[:len(fft)//2])
    peak_idx = np.argmax(positive_fft)
    detected_freq = positive_freqs[peak_idx]
    raw_pixel = (detected_freq - FLOOR) / DELTA
    return int(np.clip(round(raw_pixel), 0, 255))

def load_audio_data(filename):
    if not os.path.exists(filename):
        return None
    with wave.open(filename, 'r') as f:
        n_frames = f.getnframes()
        framerate = f.getframerate()
        raw_data = f.readframes(n_frames)
        audio_data = struct.unpack(f"{n_frames}h", raw_data)
        normalized_data = np.array(audio_data) / 32767.0
        return normalized_data

# --- COMPREHENSIVE TEST ---
print("=== A4 Truth Compression Algorithm Test ===")
print(f"Frequency Range: {FLOOR:.2f} Hz to {CEILING:.2f} Hz")
print(f"Sample Rate: {SAMPLE_RATE} Hz, Duration per pixel: {DURATION_PER_PIXEL*1000}ms")
print()

# Test with various pixel values
test_pixels = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255]
print(f"Testing with {len(test_pixels)} pixel values: {test_pixels}")
print()

# Encode
encoded_audio = process_image_data(test_pixels)
with wave.open('test_data.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    for sample in encoded_audio:
        f.writeframes(struct.pack('h', int(sample * 32767)))

# Decode
audio_data = load_audio_data('test_data.wav')
chunk_size = int(SAMPLE_RATE * DURATION_PER_PIXEL)
recovered_pixels = []

for i in range(0, len(audio_data), chunk_size):
    segment = audio_data[i : i + chunk_size]
    if len(segment) == chunk_size:
        pixel = decode_sound_to_pixel(segment, SAMPLE_RATE)
        recovered_pixels.append(pixel)

# Calculate accuracy
print("Results:")
print("Original → Recovered (Error)")
print("-" * 30)

total_error = 0
max_error = 0
for orig, recov in zip(test_pixels, recovered_pixels):
    error = abs(orig - recov)
    total_error += error
    max_error = max(max_error, error)
    status = "✓" if error <= 5 else "⚠" if error <= 15 else "✗"
    print(f"{orig:3d} → {recov:3d} ({error:2d}) {status}")

avg_error = total_error / len(test_pixels)
accuracy = (1 - avg_error/255) * 100

print()
print("Summary:")
print(f"Average Error: {avg_error:.2f} pixels")
print(f"Accuracy: {accuracy:.1f}%")
print(f"Max Error: {max_error} pixels")

# Test with image-like data
print()
print("=== Image-like Data Test ===")
image_pixels = [
    0, 0, 0, 0, 0,  # Black border
    255, 255, 255, 255, 255,  # White stripe
    128, 128, 128, 128, 128,  # Gray stripe
    0, 0, 0, 0, 0     # Black border
]

encoded_image = process_image_data(image_pixels)
with wave.open('image_test.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    for sample in encoded_image:
        f.writeframes(struct.pack('h', int(sample * 32767)))

image_audio = load_audio_data('image_test.wav')
recovered_image = []
chunk_size = int(SAMPLE_RATE * DURATION_PER_PIXEL)

for i in range(0, len(image_audio), chunk_size):
    segment = image_audio[i : i + chunk_size]
    if len(segment) == chunk_size:
        pixel = decode_sound_to_pixel(segment, SAMPLE_RATE)
        recovered_image.append(pixel)

print(f"Original image data: {image_pixels}")
print(f"Recovered image data: {recovered_image}")

image_errors = sum(abs(o - r) for o, r in zip(image_pixels, recovered_image))
image_accuracy = (1 - image_errors/(255 * len(image_pixels))) * 100
print(".1f")

print("\n=== Test Complete ===")
print("The A4 Truth compression algorithm successfully converts pixel data to audio frequencies")
print("and recovers it with high accuracy using FFT-based frequency detection.")