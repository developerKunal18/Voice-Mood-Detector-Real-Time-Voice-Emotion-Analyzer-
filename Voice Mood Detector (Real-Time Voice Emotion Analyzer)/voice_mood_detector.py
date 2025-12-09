import sounddevice as sd
import numpy as np
import time
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

SAMPLE_RATE = 44100
DURATION = 1  # analyze every 1 second

def analyze_voice(data):
    # volume (RMS)
    volume = np.sqrt(np.mean(data**2))

    # FFT to find pitch/energy
    fft = np.fft.rfft(data)
    mags = np.abs(fft)
    dominant_freq = np.argmax(mags)

    # simple rules for emotion detection
    if volume > 0.15 and dominant_freq > 3000:
        return "😱 Excited"
    elif volume > 0.17 and dominant_freq < 1500:
        return "😡 Angry"
    elif volume < 0.08 and dominant_freq < 1200:
        return "😢 Sad"
    elif 0.08 <= volume <= 0.15:
        return "😐 Neutral"
    else:
        return "😀 Happy"

def main():
    clear()
    print("🎤 Voice Mood Detector")
    print("Speak into the microphone every second...")
    print("Press CTRL + C to stop.\n")

    while True:
        try:
            data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()

            data = data.flatten()

            mood = analyze_voice(data)
            print(f"Detected Mood: {mood}")

        except KeyboardInterrupt:
            print("\nStopping...")
            break

if __name__ == "__main__":
    main()
