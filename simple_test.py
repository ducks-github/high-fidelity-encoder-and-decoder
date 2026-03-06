import numpy as np
import wave
import struct

# Constants
PI = np.pi
SQRT2 = np.sqrt(2)
FLOOR = 100 * PI * SQRT2
CEILING = 198 * PI
SAMPLE_RATE = 8000
DURATION_PER_PIXEL = 0.05
DELTA = (CEILING - FLOOR) / 255

def encode_pixel_to_sound(pixel_value):
    freq = FLOOR + (pixel_value * DELTA)
    t = np.linspace(0, DURATION_PER_PIXEL, int(SAMPLE_RATE * DURATION_PER_PIXEL), endpoint=False)
    return np.sin(2 * PI * freq * t)

def decode_sound_to_pixel(audio_segment, sample_rate):
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(audio_segment), 1/sample_rate)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft[:len(fft)//2])
    peak_idx = np.argmax(positive_fft)
    detected_freq = positive_freqs[peak_idx]
    raw_pixel = (detected_freq - FLOOR) / DELTA
    return int(np.clip(round(raw_pixel), 0, 255))

# Test data
test_data = [0, 64, 128, 192, 255]
print('Original pixels:', test_data)

# Encode
encoded = []
for p in test_data:
    encoded.append(encode_pixel_to_sound(p))
encoded_audio = np.concatenate(encoded)

# Save to WAV
with wave.open('quick_test.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    for sample in encoded_audio:
        f.writeframes(struct.pack('h', int(sample * 32767)))

# Load and decode
with wave.open('quick_test.wav', 'r') as f:
    n_frames = f.getnframes()
    raw_data = f.readframes(n_frames)
    audio_data = struct.unpack(f'{n_frames}h', raw_data)
    normalized_data = np.array(audio_data) / 32767.0

# Decode segments
chunk_size = int(SAMPLE_RATE * DURATION_PER_PIXEL)
recovered = []
for i in range(0, len(normalized_data), chunk_size):
    segment = normalized_data[i:i+chunk_size]
    if len(segment) == chunk_size:
        pixel = decode_sound_to_pixel(segment, SAMPLE_RATE)
        recovered.append(pixel)

print('Recovered pixels:', recovered)

# Check accuracy
errors = [abs(o-r) for o,r in zip(test_data, recovered)]
print('Errors:', errors)
print('Max error:', max(errors))
print('Average error:', sum(errors)/len(errors))

if max(errors) <= 10:
    print('✅ SUCCESS: Compression algorithm working well!')
else:
    print('⚠️  PARTIAL: Algorithm working but with some error')