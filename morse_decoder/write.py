class Write:
    def __init__(self):

        self.morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', 'Å': '.--.-', 'Ä': '.-.-', 'Ö': '---.',
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--', ' ': '/'
    }

    def write(self, text):
        """Takes a text as argument and returns a list with morse code"""
        text = list(text.upper())
        text_to_morse_visual = []
        for char in text:
            text_to_morse_visual.append(self.morse_code_dict[char])
        return text_to_morse_visual