import cv2
import numpy as np
import matplotlib.pyplot as plt

class Analyze:
    def __init__(self):

        self.morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '.--.-': 'Å', '.-.-': 'Ä', '---.': 'Ö',

            '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
            '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',

            '.-.-.-': '.', '--..--': ',', '..--..': '?', '-.-.--': '!'
        }

        self.filepath = 'morse_decoder/spectrogram/spectrogram.png'

        self.morse_code = []

        self.morse_sequence = []

        self.current_state = 'pause'  # Börjar med en paus
        self.current_length = 0

        self.grouped_morse = {}
        self.current_group = ""
        self.group_index = 0

    def read_spectrogram(self):
        """Returns a binary image in black and white as an array"""

        img = cv2.imread(self.filepath, cv2.IMREAD_GRAYSCALE)

        # Thresholda bilden för att få en binär version (svart/vit)
        _, binary_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

        # Hitta koordinater för alla icke-svarta pixlar
        coords = cv2.findNonZero(255 - binary_img)  # Invertera så att vi hittar vita pixlar
        x, y, w, h = cv2.boundingRect(coords)  # Hitta minsta rektangel som omsluter vita områden

        # Lägger till en säkerhetsmarginal för att ta bort oönskade kanter
        margin = 2  # Antal pixlar att ta bort från kanterna

        # Beskär bilden och lägg till marginalen
        binary_img = binary_img[y+margin:y+h-margin, x+margin:x+w-margin]

        # Visa resultatet
        # plt.subplot(1, 2, 1)
        # plt.title("Originalbild med padding")
        # plt.imshow(img, cmap='gray')

        # plt.subplot(1, 2, 2)
        plt.title("Morse Code as Spectrogram:")
        plt.xlabel('Time')
        plt.ylabel('Intensity')
        plt.xticks([])
        plt.yticks([])
        plt.imshow(binary_img, cmap='gray')

        # plt.show()

        return binary_img


    def analyze_spectrogram(self, binary_img):
        """Takes an array as input and returns a list with the length of number of beeps and pauses
        from the recording"""
        height, width = binary_img.shape
        # print(f'width: {width}')

        for x in range(width):
            column = binary_img[:, x]
            # print(f'column: {column}')# Ta en vertikal linje i bilden
            is_signal = np.any(column == 255)  # Om det finns vita pixlar (pip)

            if is_signal:
                if self.current_state == 'pause':
                    self.morse_sequence.append(('pause', self.current_length))
                    self.current_length = 1
                    self.current_state = 'pip'
                else:
                    self.current_length += 1
            else:
                if self.current_state == 'pip':
                    self.morse_sequence.append(('pip', self.current_length))
                    self.current_length = 1
                    self.current_state = 'pause'
                else:
                    self.current_length += 1

        # Lägg till sista segmentet
        self.morse_sequence.append((self.current_state, self.current_length))

        return self.morse_sequence


    def read_morse_sequence(self, morse_sequence):
        """Takes a list with tuples of beeps and pauses and their length as input
        and returns a list with beeps and pauses translated to morse signs"""
        pip_lengths = [length for state, length in morse_sequence if length >= 3 and state == 'pip']
        if pip_lengths:
            unit = min(pip_lengths)
        else:
            unit = None
        # print(f'unit: {unit}')
        # print(f'length: {binary_img.shape[1]}')

        for state, length in morse_sequence:
            units = round(length / unit)  # Omvandla pixel-längd till enheter

            if state == 'pip':
                if unit + 2 >= length >= unit > 2:
                    self.morse_code.append(".")
                elif units > 2:
                    self.morse_code.append("-")
            elif state == 'pause':
                if 2 < units < 10:
                    self.morse_code.append("/") # Mellanrum mellan bokstäver
                elif units >= 10:
                    self.morse_code.append("//")   # Mellanrum mellan ord

        return self.morse_code

    def create_morse(self, decoded_morse):
        """Takes a list with morse code as input and returns a dictionary with structured morse code"""
        # Loopa genom listan
        for symbol in decoded_morse:
            if symbol == '//':  # Nytt ord
                if self.current_group:
                    self.grouped_morse[self.group_index] = self.current_group
                    self.group_index += 1
                self.grouped_morse[self.group_index] = '//'
                self.group_index += 1
                self.current_group = ""
            elif symbol == '/':  # Ny bokstav
                if self.current_group:
                    self.grouped_morse[self.group_index] = self.current_group
                    self.group_index += 1
                self.current_group = ""
            else:
                self.current_group += symbol  # Lägg till morse-tecken

        # Lägg till sista gruppen om den finns
        if self.current_group:
            self.grouped_morse[self.group_index] = self.current_group

        return self.grouped_morse


    def decode_morse(self, decoded_morse_signs_dict):
        """Takes a dictionary as input and returns a string"""
        string = ""
        for key in decoded_morse_signs_dict:
            if decoded_morse_signs_dict[key] in self.morse_dict:
                string += self.morse_dict[decoded_morse_signs_dict[key]]
            if decoded_morse_signs_dict[key] == '//':
                string += " "

        stripped_str = string.strip()
        return stripped_str

