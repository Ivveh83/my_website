from morse_decoder.record_sound import Record
from  morse_decoder.analyze import Analyze

class Run:
    def __init__(self, choice):
        self.choice = choice

    def analyze(self):
        record = Record()
        record.create_spectrogram()
        analyze = Analyze()
        binary_morse_spectrogram = analyze.read_spectrogram()
        morse_sequence = analyze.analyze_spectrogram(binary_morse_spectrogram)
        code = analyze.read_morse_sequence(morse_sequence)
        grouped_morse_code = analyze.create_morse(code)
        morse_to_text = analyze.decode_morse(grouped_morse_code)

        return morse_to_text.capitalize()




