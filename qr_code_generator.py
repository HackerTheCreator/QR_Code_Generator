import random
import pygame
import sys
import time

from pygame import Vector2, font, Rect

import error_correction

pygame.init()
font.init()

resolution = pygame.Vector2(1400, 1400)
running = True
screen = pygame.display.set_mode((resolution.x, resolution.y))
pygame.display.set_caption("QR Code Generator")
clock = pygame.time.Clock()
tick_speed = 60



number_of_data_bits = {
    "L": [0, 152, 272, 440, 640, 864, 1088, 1248, 1552, 1856, 2192, 2592, 2960, 3424, 3688, 4184, 4712, 5176, 5768, 6360, 6888, 7456, 8048, 8752, 9392, 10208, 10960, 11744, 12448, 13048, 13880, 14744, 15640, 16568, 17528, 18448, 19472, 20528, 21616, 22496, 23648],
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
qr_ecc_groups = {
            #0   1    2    3    4     5      6     7      8       9        10      11      12      13       14       15       16       17       18       19       20        21       22       23        24        25         26      27        28        29         30       31        32        33        34        35        36       37         38       39        40
    "L": [None, [1], [1], [1], [1], [1],    [2], [2],    [2],    [2],    [2, 2], [4],    [2, 2], [4],     [3, 1],  [5, 1],  [5, 1],  [1, 5],  [5, 1],  [3, 4],  [3, 5],   [4, 4],  [2, 7],  [4, 5],   [6, 4],   [8, 4],   [10, 2], [8, 4],   [3, 10],  [7, 7],   [5, 10],  [13, 3],  [17],     [17, 1],  [13, 6],  [12, 7],  [6, 14],  [17, 4],  [4, 18],  [20, 4],  [19, 6]],
    "M": [None, [1], [1], [1], [2], [2],    [4], [4],    [2, 2], [3, 2], [4, 1], [1, 4], [6, 2], [8, 1],  [4, 5],  [5, 5],  [7, 3],  [10, 1], [9, 4],  [3, 11], [3, 13],  [17],    [17],    [4, 14],  [6, 14],  [8, 13],  [19, 4], [22, 3],  [3, 23],  [21, 7],  [19, 10], [2, 29],  [10, 23], [14, 21], [14, 23], [12, 26], [6, 34],  [29, 14], [13, 32], [40, 7],  [18, 31]],
    "Q": [None, [1], [1], [2], [2], [2, 2], [4], [2, 4], [4, 2], [4, 4], [6, 2], [4, 4], [4, 6], [8, 4],  [11, 5], [5, 7],  [15, 2], [1, 15], [17, 1], [17, 4], [15, 5],  [17, 6], [7, 16], [11, 14], [11, 16], [7, 22],  [28, 6], [8, 26],  [4, 31],  [1, 37],  [15, 25], [42, 1],  [10, 35], [29, 19], [44, 7],  [39, 14], [46, 10], [49, 10], [48, 14], [43, 22], [34, 34]],
    "H": [None, [1], [1], [2], [4], [2, 2], [4], [4, 1], [4, 2], [4, 4], [6, 2], [3, 8], [7, 4], [12, 4], [11, 5], [11, 7], [3, 13], [2, 17], [2, 19], [9, 16], [15, 10], [19, 6], [34],    [16, 14], [30, 2],  [22, 13], [33, 4], [12, 28], [11, 31], [19, 26], [23, 25], [23, 28], [19, 35], [11, 46], [59, 1],  [22, 41], [2, 64],  [24, 46], [42, 32], [10, 67], [20, 61]]
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


def Automatic_QR_Code_Version(text:str):
    for version, value in enumerate(number_of_data_bits[error_correction_level], 0):
        if version <= 9:
            padding = character_count_indicators[encoding_mode][0]
        elif 10 <= version <= 26:
            padding = character_count_indicators[encoding_mode][1]
        else: 
            padding = character_count_indicators[encoding_mode][2]

        if value >= len("".join([format(x, "08b") for x in text.encode('utf-8')])) + 4 + padding + 4:
            return version
    raise ValueError("Input Data is too big to fit inside any QR code.")





data = "Hello World" 

error_correction_level = "Q"       #L - Low(7%), M - Medium(15%), Q - Quartile(25%), H - High(30%)
masking_pattern = None
encoding_mode = "byte" #byte / alphanumeric

qr_code_version = Automatic_QR_Code_Version(data)

quiet_zone_from_borders = 100






cells_per_side = 17 + 4 * qr_code_version
cell_size = (resolution.x - quiet_zone_from_borders * 2) / cells_per_side

matrix = [None] * cells_per_side**2         #Create Image from it



def Vector2_To_Index(vector:Vector2, side_amount=cells_per_side) -> int:
    return int(side_amount * vector.y + vector.x)


def Index_To_Vector2(index:int, side_amount=cells_per_side) -> Vector2:
    return Vector2(index % side_amount, index // side_amount)


def Resize_Vector2(vector:Vector2):
    return Vector2(quiet_zone_from_borders + vector.x * cell_size + cell_size / 2, quiet_zone_from_borders + vector.y * cell_size + cell_size / 2)


def Clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def Generate_Circle_Patterns(one_side_size=9, start_with_black=False) ->list[None|bool]:
    rings_amount = 4
    finder_pattern = [None] * (one_side_size**2)
    starting_pos = Vector2(0, 0)

    for ring in range(rings_amount):
        current_ring_size = one_side_size - ring * 2
        ring += start_with_black

        for x in range(current_ring_size):
            for y in range(current_ring_size):
                finder_pattern[Vector2_To_Index(starting_pos + Vector2(x, y), one_side_size)] = False if ring % 2 == 0 else True
        starting_pos += Vector2(1, 1)

    return finder_pattern


def Visualize_QR_Code():
    adder = 2

    for index, bit in enumerate(matrix):
        color = (255, 0, 0)
        match bit:
            case True:
                color = (0, 0, 0)
            case False:
                color = (255, 255, 255)
            case Any:
                color = (0, random.randint(50, 255), 0)
        
        position = Resize_Vector2(Index_To_Vector2(index))
        pygame.draw.rect(screen, color, Rect(position.x - cell_size / 2 - adder / 2, position.y - cell_size / 2 - adder / 2, cell_size + adder, cell_size + adder))

    pygame.display.update()


def Insert_Pattern_To_Matrix(left_top_pos:Vector2, pattern:list, pattern_size):
    for index, value in enumerate(pattern):
        pattern_position = Index_To_Vector2(index, pattern_size) + left_top_pos

        if 0 <= pattern_position.x < cells_per_side and 0 <= pattern_position.y < cells_per_side:
            matrix[Vector2_To_Index(pattern_position)] = value


def Draw_Timing_Patterns():
    start_position = Vector2(1, 1) * (finder_pattern_size - 3)

    for i in range(2, cells_per_side - finder_pattern_size * 2 + 4):
        matrix[Vector2_To_Index(start_position + Vector2(1, 0) * i)] = True if i % 2 == 0 else False
        matrix[Vector2_To_Index(start_position + Vector2(0, 1) * i)] = True if i % 2 == 0 else False


def Get_Alignment_Patterns_Amount(version):
    versions = [(1, 1), (2, 6), (7, 13), (14, 20), (21, 27), (28, 34), (35, 40)]
    for index, min_max in enumerate(versions):
        if min_max[0] <= version <= min_max[1]:
            return index
    raise ValueError("QR Code's version is too high or too low. QR Code version must be between 1-40")


def Get_Alignment_Distance():
    alignment_patterns_amount = Get_Alignment_Patterns_Amount(qr_code_version)
    if alignment_patterns_amount == 0:
        return 0

    if 1 <= qr_code_version <= 6:
        return (cells_per_side - (finder_pattern_size - 2) * 2) // alignment_patterns_amount + 1
        
    versions_alignment_dst = [0, 0, 0, 0, 0, 0, 0, 16, 18, 20, 22, 24, 26, 28, 20, 22, 24, 24, 26, 28, 28, 22, 24, 24, 26, 26, 28, 28, 24, 24, 26, 26, 26, 28, 28, 24, 26, 26, 26, 28, 28]
    
    return versions_alignment_dst[qr_code_version]


def Draw_Alignment_Patterns():
    distance_between_alignment_patterns = Get_Alignment_Distance()
    if distance_between_alignment_patterns == 0:
        return

    alignment_pattern = Generate_Circle_Patterns(alignment_pattern_size, start_with_black=True)
    alignment_patterns_amount = Get_Alignment_Patterns_Amount(qr_code_version)

    start_position_from_back = Vector2(1, 1) * (cells_per_side - (finder_pattern_size - 3))

    all_x_pos = []
    for x in range(alignment_patterns_amount + 1):
        for y in range(alignment_patterns_amount):
            if x < alignment_patterns_amount:
                new_pos = start_position_from_back + Vector2(-x, -y) * (distance_between_alignment_patterns + 1)
                if matrix[Vector2_To_Index(new_pos)] == None:
                    new_pos = Vector2(new_pos.x - 2, new_pos.y - 2)
                    if new_pos.x % 2 != 0:
                        new_pos.x -= 1
                    if new_pos.y % 2 != 0:
                        new_pos.y -= 1
                    Insert_Pattern_To_Matrix(new_pos, alignment_pattern.copy(), alignment_pattern_size)

                if x == 0:
                    all_x_pos.append(new_pos)

    
    for i in all_x_pos[1:]:  
        if matrix[Vector2_To_Index(Vector2(i.y, 0))] == None:
            Insert_Pattern_To_Matrix(Vector2(i.y, 4), alignment_pattern.copy(), alignment_pattern_size)

        if matrix[Vector2_To_Index(Vector2(0, i.y))] == None:
            Insert_Pattern_To_Matrix(Vector2(4, i.y), alignment_pattern.copy(), alignment_pattern_size)


def Bit_Division(bits, polynomial, final_size=10):
    new_bits = bits

    while len(bin(new_bits)) - 2 >= final_size + 1:
        new_bits ^= polynomial << (len(bin(new_bits)) - 2 - (len(bin(polynomial)) - 2))

    return new_bits


def Generate_Draw_Version_Info():
    if qr_code_version <= 6:
        return
    
    polynomial = 0b1111100100101
    ver_info = qr_code_version

    ver_info <<= 12 #bit amount to 18
    
    ver_info = Bit_Division(ver_info, polynomial, 12)   #generates error correction bits to the version info

    ver_info = list(reversed(format(qr_code_version, "06b") + format(ver_info, "012b")))    #add version + error correction together

    start_pos = Vector2(0, cells_per_side - 11)
    for x in range(6):
        for y in range(3):
            matrix[Vector2_To_Index(start_pos + Vector2(x, y))] = bool(int(ver_info[x * 3 + y]))
    
    start_pos = Vector2(cells_per_side - 11, 0)
    for y in range(6):
        for x in range(3):
            matrix[Vector2_To_Index(start_pos + Vector2(x, y))] = bool(int(ver_info[y * 3 + x]))


def Generate_Draw_Format_Info(using_masking_pattern:int, using_matrix:list[bool]):
    match error_correction_level:
        case "L":
            ecl = 1
        case "M":
            ecl = 0
        case "Q":
            ecl = 3
        case "H":
            ecl = 2
        case _:
            raise ValueError("Error Correction Level Error: Wrong Set Value.")

    polynomial = 0b10100110111

    ecl_masking = format(ecl, "02b") + format(using_masking_pattern, "03b")
    format_info = int(ecl_masking, 2)
    format_info <<= 10  #change bits amount to 15


    format_info = Bit_Division(format_info, polynomial, 10)     #generates error correction bits to the format info

    format_info = ecl_masking + format(format_info, "010b")     #adds ecl and masking to the front of format informations
    format_info = int(format_info, 2)
    format_info ^= 0b101010000010010    #finally XOR with this specific number

    #First line
    using_matrix[Vector2_To_Index(Vector2(8, cells_per_side - 8))] = True    #Dark module
    for i, bit in enumerate(format(format_info, "015b")):
        if i <= 6:
            using_matrix[Vector2_To_Index(Vector2(8, cells_per_side - 1 - i))] = bool(int(bit))
        else:
            using_matrix[Vector2_To_Index(Vector2(cells_per_side - 15 + i, 8))] = bool(int(bit))

    #Second line
    for i in range(6):
        using_matrix[Vector2_To_Index(Vector2(i, 8))] = bool(int(format(format_info, "015b")[i]))
        using_matrix[Vector2_To_Index(Vector2(8, i))] = bool(int(format(format_info, "015b")[-i - 1]))

    using_matrix[Vector2_To_Index(Vector2(8, 7))] = bool(int(format(format_info, "015b")[8]))
    using_matrix[Vector2_To_Index(Vector2(8, 8))] = bool(int(format(format_info, "015b")[7]))
    using_matrix[Vector2_To_Index(Vector2(7, 8))] = bool(int(format(format_info, "015b")[6]))


def Draw_Masking_Pattern():
    formula = None
    match masking_pattern:
        case 0:
            formula = lambda x, y: (x + y) % 2 == 0
        case 1:
            formula = lambda x, y: y % 2 == 0
        case 2:
            formula = lambda x, y: x % 3 == 0
        case 3:
            formula = lambda x, y: (x + y) % 3 == 0
        case 4:
            formula = lambda x, y: (y // 2 + x // 3) % 2 == 0
        case 5:
            formula = lambda x, y: (x * y) % 2 + (x * y) % 3 == 0
        case 6:
            formula = lambda x, y: ((x * y) % 3 + x * y) % 2 == 0
        case 7:
            formula = lambda x, y: ((x * y) % 3 + x + y) % 2 == 0
        case _:
            raise ValueError("Masking Error: Wrong Masking Value.")
    
    for i, val in enumerate(matrix):
        if val == None:
            pos = Index_To_Vector2(i)
            matrix[i] = formula(pos.x, pos.y)


def Masking(pos:Vector2, using_masking_pattern) -> bool:
    formula = None
    match using_masking_pattern:
        case 0:
            formula = lambda x, y: (x + y) % 2 == 0
        case 1:
            formula = lambda x, y: y % 2 == 0
        case 2:
            formula = lambda x, y: x % 3 == 0
        case 3:
            formula = lambda x, y: (x + y) % 3 == 0
        case 4:
            formula = lambda x, y: (y // 2 + x // 3) % 2 == 0
        case 5:
            formula = lambda x, y: (x * y) % 2 + (x * y) % 3 == 0
        case 6:
            formula = lambda x, y: ((x * y) % 3 + x * y) % 2 == 0
        case 7:
            formula = lambda x, y: ((x * y) % 3 + x + y) % 2 == 0
        case _:
            raise ValueError("Masking Error: Wrong Masking Value.")
    return formula(pos.x, pos.y)


def Get_Free_Bit_Space(version:int):
    blocks_per_side = 17 + 4 * version
    
    finder_patterns = 8 * 8 * 3

    version_infos = 0 if version <= 6 else 2 * 3 * 6

    alignment_patterns_amount = Get_Alignment_Patterns_Amount(version)
    alignment_patterns = alignment_patterns_amount ** 2 * 5 * 5 + (alignment_patterns_amount - 1) * 2 * 4 * 5 if alignment_patterns_amount != 0 else 0

    timing_patterns = 2 * (blocks_per_side - 2 * 8)

    return blocks_per_side ** 2 - finder_patterns - version_infos - alignment_patterns - timing_patterns - 31


def Encode_To_Alphanumeric(text:str):
    alphanumeric_dict = {
        '0': 0,  '1': 1,  '2': 2,  '3': 3,  '4': 4,  '5': 5,  '6': 6,  '7': 7,  '8': 8,  '9': 9,   # 0-9
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 
        'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 
        'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35,                                      # A-Z (10-35)
        ' ': 36, '$': 37, '%': 38, '*': 39, '+': 40, '-': 41, '.': 42, '/': 43, ':': 44           # Special (36-44)
    }

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

    text = text.replace("\n", "")

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

    encoded_text += "0" * min(4, number_of_data_bits[error_correction_level][qr_code_version] - len(encoded_text))
    encoded_text += "0" * (-len(encoded_text) % 8)

    encoding_pad_bytes = "1110110000010001"

    index = 0
    for _ in range(number_of_data_bits[error_correction_level][qr_code_version] - len(encoded_text)):
        encoded_text += encoding_pad_bytes[index]
        
        index += 1
        if index >= 16:
            index = 0
    decimal_nums = [int(encoded_text[x:Clamp(x+8, 0, len(encoded_text))], 2) for x in range(0, len(encoded_text), 8)]
    #print("  ".join([encoded_text[x:Clamp(x+8, 0, len(encoded_text))] for x in range(0, len(encoded_text), 8)]))
    return decimal_nums


def Split_Data(data_in_decimal:list[int]):
    data_per_block = len(data_in_decimal) // sum(qr_ecc_groups[error_correction_level][qr_code_version])
    splited_data = []
    using_group = qr_ecc_groups[error_correction_level][qr_code_version][0]

    ec_bytes_amount_per_block = (Get_Free_Bit_Space(qr_code_version) - number_of_data_bits[error_correction_level][qr_code_version]) // (8 * sum(qr_ecc_groups[error_correction_level][qr_code_version]))

    ec = error_correction.Error_Correction()

    last_index = 0
    block_index = 0
    while last_index < sum(qr_ecc_groups[error_correction_level][qr_code_version]):
        new_data = data_in_decimal[block_index:block_index + data_per_block]
        splited_data.append([new_data, ec.Generate_Error_Correction(new_data, None, None, ec_bytes_amount_per_block)])
        
        last_index += 1
        block_index += data_per_block

        if last_index == using_group:
            data_per_block += 1

    return splited_data


def Blocks_Interleaving(splited_data:list[list[list[int], list[int]]]) -> tuple[list[int], list[int]]:
    def Loop(using_list:list[int], using_index:int):
        new_interleaved_codewords = []

        all_codewords = [x[using_index] for x in using_list]
        for i in range(len(using_list[-1][using_index])):
            for codeword in all_codewords:
                if i < len(codeword):
                    new_interleaved_codewords.append(codeword[i])
        return new_interleaved_codewords

    return Loop(splited_data, 0), Loop(splited_data, 1)


def Insert_Encoded_Data_Into_Matrix(using_matrix:list[bool], encoded_data:str, using_masking_pattern:int):
    movement_vector = Vector2(0, -1)
    index = 0
    current_pos = Vector2(cells_per_side - 1, cells_per_side - 1)

    while index < len(encoded_data):
        if index != 0 and (current_pos.y <= -1 or current_pos.y >= cells_per_side):
            movement_vector *= -1

            if current_pos.x == 8:  #Vertical Timing Exception
                current_pos.x -= 1

            current_pos.y = Clamp(current_pos.y, 0, cells_per_side - 1)
            current_pos.x -= 2
            

        if using_matrix[Vector2_To_Index(current_pos)] is None:
            new_data = bool(int(encoded_data[index]))
            new_data = not new_data if Masking(current_pos, using_masking_pattern) == True else new_data

            using_matrix[Vector2_To_Index(current_pos)] = new_data
            index += 1

        if using_matrix[Vector2_To_Index(Vector2(current_pos.x - 1, current_pos.y))] is None:
            new_data = bool(int(encoded_data[index]))
            new_data = not new_data if Masking(Vector2(current_pos.x - 1, current_pos.y), using_masking_pattern) == True else new_data

            using_matrix[Vector2_To_Index(Vector2(current_pos.x - 1, current_pos.y))] = new_data
            index += 1

        current_pos += movement_vector


def Masking_Evaluation(using_matrix:list[bool]) -> int:
    penalty_score = 0

    def Rotate_Index(index:int, rotate:bool):
        if rotate:
            old_vector = Index_To_Vector2(index)
            return Vector2_To_Index(Vector2(old_vector.y, old_vector.x))
        return index

    def First_Evaluation():
        score = 0
        new_score = 0
        for i in range(2):
            
            using_module = 0
            module_amount_of_same_color = 0
            for index in range(len(using_matrix)):
                if using_matrix[Rotate_Index(index, i == 1)] == using_matrix[using_module] and Index_To_Vector2(index).y == Index_To_Vector2(using_module).y:
                    module_amount_of_same_color += 1
                else:
                    if module_amount_of_same_color >= 5:
                        new_score += module_amount_of_same_color - 2
                    module_amount_of_same_color = 1
                    using_module = Rotate_Index(index, i == 1)
            score += new_score
        return score

    def Second_Evaluation():
        score = 0
        for i, value in enumerate(using_matrix):
            if using_matrix[min(len(using_matrix) - 1, i + 1)] == value and using_matrix[min(len(using_matrix) - 1, i + cells_per_side)] == value and using_matrix[min(len(using_matrix) - 1, i + 1 + cells_per_side)] == value:
                score += 3
        return score
    
    def Third_Evaluation():
        testing_list = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
        score = 0
        for i in range(len(using_matrix)):
            pos = Index_To_Vector2(i)
            if using_matrix[i:len(testing_list) - 1 + i] == testing_list or using_matrix[i:len(testing_list) - 1 + i] == reversed(testing_list):
                score += 40

        return score

    def Fourth_Evaluation():
        module_amount = cells_per_side**2
        dark_module_amount = len(list(filter(lambda x: x == True, using_matrix)))
        percentage = (dark_module_amount / module_amount) * 100
        first = percentage - percentage % 5
        second = percentage + 4 
        first = abs(first - 50) // 5
        second = abs(second - 50) // 5
        if first <= second:
            return first * 10
        else:
            return second * 10

    penalty_score = First_Evaluation() + Second_Evaluation() + Third_Evaluation() + Fourth_Evaluation()

    return penalty_score



screen.fill((255, 255, 255))
last_time = time.time()

alignment_pattern_size = 5
finder_pattern_size = 9
finder_pattern = Generate_Circle_Patterns(finder_pattern_size, start_with_black=False)

Insert_Pattern_To_Matrix(Vector2(-1, -1), finder_pattern.copy(), finder_pattern_size)
Insert_Pattern_To_Matrix(Vector2(-1, cells_per_side + 1 - finder_pattern_size), finder_pattern.copy(), finder_pattern_size)
Insert_Pattern_To_Matrix(Vector2(cells_per_side + 1 - finder_pattern_size, -1), finder_pattern.copy(), finder_pattern_size)

Draw_Alignment_Patterns()

Draw_Timing_Patterns()

Generate_Draw_Version_Info()

encoded_data = Encode_Text(data)

splited_data = Split_Data(encoded_data)
data_codewords, ec_codewords = Blocks_Interleaving(splited_data)

final_message = ''.join([format(x, '08b') for x in data_codewords + ec_codewords])

reminder_bits_amount = Get_Free_Bit_Space(qr_code_version) - len(final_message)
if reminder_bits_amount < 0:
    raise MemoryError("Imported Data are way too big for this qr code version and it's error correction level")
final_message += "0" * reminder_bits_amount

#Draw_Masking_Pattern()

if masking_pattern is None: #masking evaluation
    all_evaluation_matrixs = []
    for i in range(0, 8):
        using_matrix = matrix.copy()
        Generate_Draw_Format_Info(i, using_matrix)
        Insert_Encoded_Data_Into_Matrix(using_matrix, final_message, i)

        penalty_index = Masking_Evaluation(using_matrix)
        all_evaluation_matrixs.append((using_matrix, penalty_index, i))

    lowest_penalty_scored_matrix = sorted(all_evaluation_matrixs, key=lambda x: x[1])[0]

    matrix = lowest_penalty_scored_matrix[0]
    masking_pattern = lowest_penalty_scored_matrix[2]
else:
    Generate_Draw_Format_Info(masking_pattern, matrix)
    Insert_Encoded_Data_Into_Matrix(matrix, final_message, masking_pattern)

Visualize_QR_Code()

print(f"Done: {round(time.time() - last_time, 4)}s")

print(f"""------------------------------
Version {qr_code_version}: {cells_per_side}x{cells_per_side} 
Error Correction Level: {error_correction_level}
Encoding Mode: {encoding_mode}
Masking Pattern: {masking_pattern}
------------------------------""")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                sys.exit()
    
    clock.tick(tick_speed)
    pygame.display.update()