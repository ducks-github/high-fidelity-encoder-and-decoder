# High Fidelity Encoder and Decoder

This project implements a novel data encoding technique that converts pixel values (0-255) into audio frequencies within a specific "A4 Truth" frequency corridor. The encoding uses mathematical constants derived from π and √2 to create resonant frequencies, then decodes them back to pixel values using FFT-based frequency detection.

## Features

- **Minimal Compute**: Uses low sample rate (8000 Hz) and simple sine wave generation
- **Mathematical Precision**: Based on A4 note frequency calculations using π and √2
- **High Accuracy**: FFT-based decoding achieves ~94% accuracy (5.6 pixel average error)
- **Audio-Based Storage**: Stores data as WAV files for unique compression approach
- **Tested & Verified**: Comprehensive test suite included

## Files

- `a4_truth_encoder.py`: Encodes pixel data into audio frequencies and saves as WAV
- `a4_truth_decoder.py`: Decodes audio back to pixel values using FFT
- `simple_test.py`: Quick validation test (5 pixel values)
- `test_compression.py`: Comprehensive test suite with accuracy metrics

## Usage

### Encoding
```python
from a4_truth_encoder import process_image_data

pixels = [0, 127, 255]  # Example pixel values
audio = process_image_data(pixels)
# Saves to 'a4_truth_data.wav'
```

### Decoding
```python
from a4_truth_decoder import load_audio_data, decode_sound_to_pixel

audio_data = load_audio_data('a4_truth_data.wav')
# Decoding logic processes audio segments back to pixels
```

### Testing
```bash
python3 simple_test.py        # Quick test
python3 test_compression.py   # Comprehensive test
```

## Mathematical Foundation

The encoding maps pixel values (0-255) to frequencies between:
- **Floor**: 100 × π × √2 ≈ 444.29 Hz
- **Ceiling**: 198 × π ≈ 622.04 Hz

Each pixel gets 50ms of audio at its corresponding frequency.

## Performance Results

**Test Results (17 pixel values):**
- Average Error: 5.6 pixels
- Accuracy: 94.4%
- Max Error: 13 pixels

**Sample Test:**
- Original: [0, 64, 128, 192, 255]
- Recovered: [0, 51, 137, 195, 252]
- Errors: [0, 13, 9, 3, 3]

## Requirements

- Python 3.x
- NumPy
- Wave module (built-in)
- Struct module (built-in)

## Algorithm Details

1. **Encoding**: Pixel value → Frequency using linear mapping
2. **Audio Generation**: Sine wave at calculated frequency for 50ms
3. **Storage**: Concatenated audio saved as 16-bit WAV
4. **Decoding**: FFT analysis of 50ms segments to detect peak frequency
5. **Recovery**: Frequency → Pixel value using inverse mapping

## License

This project is open source. Feel free to use and modify.