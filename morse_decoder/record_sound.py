import time

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from librosa import feature
import librosa.display
import matplotlib.pyplot as plt
import librosa
import os

class Record:
    def __init__(self):
        # Filnamn för WAV-filen
        self.filename = 'morse_decoder/audio/audio_recording.wav'
        self.spectrogram_filename = 'morse_decoder/spectrogram/spectrogram.png'
        # Samplingsfrekvens
        self.samplerate = 44100

    def record(self, length:int):
        """Takes an input (int) as 'length' (number of seconds to record)"""

        # Kontrollera om mappen 'audio' finns, annars skapa den
        if not os.path.exists('morse_decoder/audio/'):
            os.makedirs('morse_decoder/audio/')

        # Spela in ljud från mikrofonen
        print("Recording sound...")
        audio = sd.rec(int(self.samplerate * length), samplerate=self.samplerate, channels=1, dtype=np.float32)
        sd.wait()

        # Spara ljudet som WAV-fil
        wav.write(self.filename, self.samplerate, (audio * 32767).astype(np.int16))  # Omvandla till 16-bitars data

        print(f"Sound recorded and saved as {self.filename}")
    def create_spectrogram(self):
        """Create and save a spectrogram"""
        # Läs in WAV-filen och skapa spektrogram med librosa
        print("Creating spectrogram...")

        # Ladda ljudfilen med librosa (detta returnerar en float32 array)
        y, sr = librosa.load(self.filename, sr=self.samplerate)

        # Skapa ett spektrogram (log-mel-spektrogram)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

        # Omvandla till decibel (logaritmisk skala)
        S_dB = librosa.power_to_db(S, ref=np.max, top_db=18)

        # Plotta spektrogrammet
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr)
        plt.xticks([])  # Ta bort ticks på x-axeln
        plt.yticks([])  # Ta bort ticks på y-axeln
        plt.xlabel('')  # Ta bort x-axelns etikett
        plt.ylabel('')  # Ta bort y-axelns etikett
        # plt.title("Spektrogram")
        # plt.colorbar(format='%+2.0f dB')
        # plt.xlabel("Tid [s]")
        # plt.ylabel("Frekvens [Hz]")


        # Kontrollera om mappen 'recorded_file_spectrogram' finns, annars skapa den
        if not os.path.exists('morse_decoder/spectrogram/'):
            os.makedirs('morse_decoder/spectrogram/')

        # Spara spektrogrammet som en PNG-fil

        plt.savefig(self.spectrogram_filename)

        print(f"Spectrogram saved as {self.spectrogram_filename}")

        # Visa spektrogrammet
        # plt.show()
