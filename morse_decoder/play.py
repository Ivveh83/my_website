import simpleaudio as sa
from time import sleep

class Play:
    def __init__(self):

        self.chars_dict = {
            'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H',
            'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P',
            'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
            'Y': 'Y', 'Z': 'Z', 'Å': 'Å', 'Ä': 'Ä', 'Ö': 'Ö',
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
            '8': '8', '9': '9',
            '.': '.', ',': ',', '!': '!', '?': 'question_mark', ' ': ' '
        }

    def play(self, text):
        """Takes a string text as input and plays up a morse code with audio"""
        text_as_list = list(text.upper())
        text_to_morse_audio = []
        for char in text_as_list:
            text_to_morse_audio.append(self.chars_dict[char])

        for char in text_to_morse_audio:
            print(char)
            if char == ' ':
                sleep(0.7)
            else:
                sleep(0.1)
                wave_obj = sa.WaveObject.from_wave_file(f"morse_decoder/wav_files/{char}.wav")
                play_obj = wave_obj.play()
                play_obj.wait_done()