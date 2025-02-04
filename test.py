text = "HELLO WORLD"
qr_code_version = 1
encoding_mode = "alphanumeric"
error_correction_level = "M"

def Clamp(value, min, max):
    if value > max:
        return max
    elif value < min:
        return min
    return value


alphanumeric_dict = {
        '0': 0,  '1': 1,  '2': 2,  '3': 3,  '4': 4,  '5': 5,  '6': 6,  '7': 7,  '8': 8,  '9': 9,   # 0-9
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 
        'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 
        'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35,                                      # A-Z (10-35)
        ' ': 36, '$': 37, '%': 38, '*': 39, '+': 40, '-': 41, '.': 42, '/': 43, ':': 44           # Special (36-44)
    }
number_of_data_bits = {
    "L": [0, 152, 272, 440, 640, 864, 1088, 1248, 1552, 1856, 2192, 2592, 2960, 3424, 3688, 4184, 4712, 5176, 5768, 6360, 6888, 7456, 8048, 8752, 9392, 10208, 10960, 11744, 12448, 13048, 13880, 14744, 15640, 16568, 17528, 18448, 19472, 20528, 21616, 22496, 23648],
    "M": [0, 128, 224, 352, 512, 688, 864, 992,   1232, 1456, 1728, 2032, 2320, 2672, 2920, 3320, 3624, 4056, 4504, 5016, 5352, 5712, 6256, 6880, 7312, 8000, 8496, 9024,     9544, 10136, 10984, 11640, 12328, 13048, 13800, 14496, 15312, 15936, 16816, 17728, 18672],
    "Q": [0, 104, 176, 272, 384, 496, 608, 704,    880, 1056, 1232, 1440, 1648, 1952, 2088, 2360, 2600, 2936, 3176, 3560, 3880, 4096, 4544, 4912, 5312, 5744, 6032, 6464,     6968, 7288, 7880, 8264,     8920, 9368, 9848, 10288, 10832, 11408, 12016, 12656, 13328],
    "H": [0, 72, 128, 208, 288, 368, 480, 528,     688, 800, 976, 1120, 1264, 1440, 1576, 1784, 2024,   2264, 2504, 2728, 3080, 3248, 3536, 3712, 4112, 4304, 4768, 5024,     5288, 5608, 5960, 6344,     6760, 7208, 7688, 7888, 8432, 8768, 9136, 9776, 10208],
}
character_count_indicators = {
    "numeric": [10, 12, 14],
    "alphanumeric": [9, 11, 13],
    "byte": [8, 16, 16],
    "kanji": [8, 10, 12]
}
mode_name_to_mode_indicator = {
    "numeric": 1,
    "alphanumeric": 2,
    "byte": 4,
    "kanji": 8,
    "eci": 7
}
 

def Encode_To_Alphanumeric(text:str):

    final_bits = ""
    text = text.upper()
    
    for index in range(0, len(text), 2):
        if index == len(text) - 1:
            final_bits += format(alphanumeric_dict[text[index]], "06b")
        else:
            final_bits += format(45 * alphanumeric_dict[text[index]] + alphanumeric_dict[text[index + 1]], "011b")
    return final_bits


def Encode_Text(text:str):
    text_lenght = len(text)

    if qr_code_version <= 9:
        padding = character_count_indicators[encoding_mode][0]
    elif 10 <= qr_code_version <= 26:
        padding = character_count_indicators[encoding_mode][1]
    else: 
        padding = character_count_indicators[encoding_mode][2]

    encoding = mode_name_to_mode_indicator[encoding_mode] << padding
    encoding += text_lenght

    binary_text = ""
    match encoding_mode:
        case "byte":
            binary_text = ''.join([format(x, '08b') for x in text.encode('utf-8')])
        case "alphanumeric":
            binary_text = Encode_To_Alphanumeric(text)
        case "numeric":
            raise TypeError("Wrong set encoding mode")
        case "kanji":
            raise TypeError("Wrong set encoding mode")
        case _:
            raise TypeError("Wrong set encoding mode")

    encoded_text = format(encoding, f"0{padding + 4}b") + binary_text

    terminator_addition = 8 - len(encoded_text) % 8
    terminator_addition = 0 if terminator_addition == 8 else terminator_addition

    encoded_text += "0" * terminator_addition

    encoding_pad_bytes = "1110110000010001"

    index = 0
    for _ in range(number_of_data_bits[error_correction_level][qr_code_version] - len(encoded_text)):
        encoded_text += encoding_pad_bytes[index]
        
        index += 1
        if index >= 16:
            index = 0
    print([int(encoded_text[x:Clamp(x+8, 0, len(encoded_text))], 2) for x in range(0, len(encoded_text), 8)])
    print("  ".join([encoded_text[x:Clamp(x+8, 0, len(encoded_text))] for x in range(0, len(encoded_text), 8)]))
    return encoded_text


print(Encode_Text(text))