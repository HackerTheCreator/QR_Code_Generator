import math

encoding_mode = "byte"
ecl = "Q"
text = "https://cs.wikipedia.org/wiki/QR_k%C3%B3d"
qr_code_version = 1

number_of_data_bits = {
    "L": [0, 152, 272, 440, 640, 864, 1088, 1248, 1552, 1856, 2192, 2592, 2960, 3424, 3688, 4184, 4712, 5176, 5768, 6360, 6888, 7456, 8048, 8752, 9392, 10208, 10960, 11744, 12248, 13048, 13880, 14744, 15640, 16568, 17528, 18448, 19472, 20528, 21616, 22496, 23648],
    "M": [0, 128, 224, 352, 512, 688, 864, 992,   1232, 1456, 1728, 2032, 2320, 2672, 2920, 3320, 3624, 4056, 4504, 5016, 5352, 5712, 6256, 6880, 7312, 8000, 8496, 9024,     9544, 10136, 10984, 11640, 12328, 13048, 13800, 14496, 15312, 15936, 16816, 17728, 18672],
    "Q": [0, 104, 176, 272, 384, 496, 608, 704,    880, 1056, 1232, 1440, 1648, 1952, 2088, 2360, 2600, 2936, 3176, 3560, 3880, 4096, 4544, 4912, 5312, 5744, 6032, 6464,     6968, 7288, 7880, 8264,     8920, 9368, 9848, 10288, 10832, 11408, 12016, 12656, 13328],
    "H": [0, 72, 128, 208, 288, 368, 480, 528,     688, 800, 976, 1120, 1264, 1440, 1576, 1784, 2024,   2264, 2504, 2728, 3080, 3248, 3536, 3712, 4112, 4304, 4768, 5024,     5288, 5608, 5960, 6344,     6760, 7208, 7688, 7888, 8432, 8768, 9136, 9776, 10208],
}
error_correction_blocks = {
    "L": [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],
    "M": [0, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],
    "Q": [0, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68],
    "H": [0, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81]
}


character_count_indicators = {
        "numeric": [10, 12, 14],
        "alphanumeric": [9, 11, 13],
        "byte": [8, 16, 16],
        "kanji": [8, 10, 12]
    }

def Get_Alignment_Patterns_Amount(version):
    versions = [(1, 1), (2, 6), (7, 13), (14, 20), (21, 27), (28, 34), (35, 40)]
    for index, min_max in enumerate(versions):
        if min_max[0] <= version <= min_max[1]:
            return index
    raise ValueError("QR Code's version is too high or too low. QR Code version must be between 1-40")


def Get_Free_Bit_Space(version:int):
    blocks_per_side = 17 + 4 * version
    
    finder_patterns = 8*8*3

    version_infos = 0 if version <= 6 else 2*3*6

    alignment_patterns_amount = Get_Alignment_Patterns_Amount(version)
    alignment_patterns = alignment_patterns_amount ** 2 * 5 * 5 + (alignment_patterns_amount - 1) * 2 * 4 * 5 if alignment_patterns_amount != 0 else 0

    timing_patterns = 2 * (blocks_per_side - 2 * 8)

    return blocks_per_side ** 2 - finder_patterns - version_infos - alignment_patterns - timing_patterns


def Get_Encoding_Mode():
    
    mode_name_to_mode_indicator = {"numeric": 1,
                                   "alphanumeric": 2,
                                   "byte": 4,
                                   "kanji": 8,
                                   "eci": 7
    }
    encoding = ""
    text_lenght = len(text)


    if qr_code_version <= 9:
        padding = character_count_indicators[encoding_mode][0]
    elif 10 <= qr_code_version <= 26:
        padding = character_count_indicators[encoding_mode][1]
    else: 
        padding = character_count_indicators[encoding_mode][2]

    encoding = mode_name_to_mode_indicator[encoding_mode] << padding
    encoding += text_lenght
    
    return format(encoding, f"0{padding + 4}b")


for version, value in enumerate(number_of_data_bits[ecl], 0):
    if version <= 9:
        padding = character_count_indicators[encoding_mode][0]
    elif 10 <= version <= 26:
        padding = character_count_indicators[encoding_mode][1]
    else: 
        padding = character_count_indicators[encoding_mode][2]

    if value >= len("".join([format(x, "08b") for x in text.encode('utf-8')])) + 4 + padding + 4:
        qr_code_version = version
        break

"""for i in range(1, 41):
    print(f"Version {i} EC = {math.floor((Get_Free_Bit_Space(i) - 31 - number_of_data_bits[ecl][i]) / 8) / error_correction_blocks[ecl][i]}")
"""

encoded_text = Get_Encoding_Mode() + ''.join([format(x, '08b') for x in text.encode('utf-8')]) + "0000"

encoded_text_size = len(encoded_text)

encoding_pad_bytes = "1110110000010001"

index = 0
for i in range(number_of_data_bits[ecl][qr_code_version] - encoded_text_size):
    encoded_text += encoding_pad_bytes[index]
    
    index += 1
    if index >= 16:
        index = 0

print(f"""QR Code Version: {qr_code_version}, ECL: {ecl}, unused_bits: {Get_Free_Bit_Space(qr_code_version)}, data_size: {number_of_data_bits[ecl][qr_code_version]}, used_data_size {encoded_text_size},
Data: {encoded_text}""")    

#EC bytes: {math.floor((Get_Free_Bit_Space(qr_code_version) - 31 - number_of_data_bits[ecl][qr_code_version]) / 8) / error_correction_blocks[ecl][qr_code_version]}