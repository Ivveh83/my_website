from morse_decoder.write import Write
from morse_decoder.play import Play
from morse_decoder.record_sound import Record
from  morse_decoder.analyze import Analyze
import time

class Run:
    def __init__(self, choice, text, record_time = 10):
        self.choice = choice
        self.text = text
        self.writing_text = Write()
        self.text_to_morse = self.writing_text.write(self.text)
        # print(f"Morse Code: {text_to_morse}")


    def play(self):



        play_text = Play()
        play_text.play(self.text)

    def analyze(self):
        analyze = Analyze()
        binary_morse_spectrogram = analyze.read_spectrogram()
        morse_sequence = analyze.analyze_spectrogram(binary_morse_spectrogram)
        code = analyze.read_morse_sequence(morse_sequence)
        grouped_morse_code = analyze.create_morse(code)
        morse_to_text = analyze.decode_morse(grouped_morse_code)

        return morse_to_text.capitalize()




