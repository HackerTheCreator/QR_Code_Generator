import random
import pygame
import sys
import time
import math

from pygame import Vector2, font, Rect

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


data = "https://cs.wikipedia.org/wiki/QR_k%C3%B3d"

error_correction_level = "Q"       #L - Low(7%), M - Medium(15%), Q - Quartile(25%), H - High(30%)
masking_pattern = 0
encoding_mode = "byte"

qr_code_version = Automatic_QR_Code_Version(data)

quiet_zone_from_borders = 20

cells_per_side = 17 + 4 * qr_code_version
print(f"""------------------------------
Version {qr_code_version}: {cells_per_side}x{cells_per_side} 
Error Correction Level: {error_correction_level}
Encoding Mode: Byte
Masking Pattern: {masking_pattern}
------------------------------""")
cell_size = (resolution.x - quiet_zone_from_borders * 2) / cells_per_side

matrix = [None] * cells_per_side**2         #Create Image from it


def Vector2_To_Index(vector:Vector2, side_amount=cells_per_side) -> int:
    return int(side_amount * vector.y + vector.x)


def Index_To_Vector2(index:int, side_amount=cells_per_side) -> Vector2:
    return Vector2(index % side_amount, index // side_amount)


def Resize_Vector2(vector:Vector2):
    return Vector2(quiet_zone_from_borders + vector.x * cell_size + cell_size / 2, quiet_zone_from_borders + vector.y * cell_size + cell_size / 2)


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


def Generate_Draw_Format_Info():
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

    ecl_masking = format(ecl, "02b") + format(masking_pattern, "03b")
    format_info = int(ecl_masking, 2)
    format_info <<= 10  #change bits amount to 15


    format_info = Bit_Division(format_info, polynomial, 10)     #generates error correction bits to the format info

    format_info = ecl_masking + format(format_info, "010b")     #adds ecl and masking to the front of format informations
    format_info = int(format_info, 2)
    format_info ^= 0b101010000010010    #finally XOR with this specific number

    #First line
    matrix[Vector2_To_Index(Vector2(8, cells_per_side - 8))] = True    #Dark module
    for i, bit in enumerate(format(format_info, "015b")):
        if i <= 6:
            matrix[Vector2_To_Index(Vector2(8, cells_per_side - 1 - i))] = bool(int(bit))
        else:
            matrix[Vector2_To_Index(Vector2(cells_per_side - 15 + i, 8))] = bool(int(bit))

    #Second line
    for i in range(6):
        matrix[Vector2_To_Index(Vector2(i, 8))] = bool(int(format(format_info, "015b")[i]))
        matrix[Vector2_To_Index(Vector2(8, i))] = bool(int(format(format_info, "015b")[- i - 1]))

    matrix[Vector2_To_Index(Vector2(8, 7))] = bool(int(format(format_info, "015b")[6]))
    matrix[Vector2_To_Index(Vector2(8, 8))] = bool(int(format(format_info, "015b")[7]))
    matrix[Vector2_To_Index(Vector2(7, 8))] = bool(int(format(format_info, "015b")[8]))


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


def Get_Free_Bit_Space(version:int):
    blocks_per_side = 17 + 4 * version
    
    finder_patterns = 8 * 8 * 3

    version_infos = 0 if version <= 6 else 2 * 3 * 6

    alignment_patterns_amount = Get_Alignment_Patterns_Amount(version)
    alignment_patterns = alignment_patterns_amount ** 2 * 5 * 5 + (alignment_patterns_amount - 1) * 2 * 4 * 5 if alignment_patterns_amount != 0 else 0

    timing_patterns = 2 * (blocks_per_side - 2 * 8)

    return blocks_per_side ** 2 - finder_patterns - version_infos - alignment_patterns - timing_patterns - 31


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

    encoded_text = format(encoding, f"0{padding + 4}b") + ''.join([format(x, '08b') for x in text.encode('utf-8')]) + "0000"

    encoding_pad_bytes = "1110110000010001"

    index = 0
    for _ in range(number_of_data_bits[error_correction_level][qr_code_version] - len(encoded_text)):
        encoded_text += encoding_pad_bytes[index]
        
        index += 1
        if index >= 16:
            index = 0

    return encoded_text


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
Generate_Draw_Format_Info()

print(Get_Free_Bit_Space(qr_code_version))
print(f"Encoded data: {Encode_Text(data)}")


# Draw_Masking_Pattern()


Visualize_QR_Code()

print(f"Done: {time.time() - last_time}s")

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