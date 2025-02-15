from copy import deepcopy
import math

primitive_polynomial = 0b100011101



def Get_Alignment_Patterns_Amount(version):
    versions = [(1, 1), (2, 6), (7, 13), (14, 20), (21, 27), (28, 34), (35, 40)]
    for index, min_max in enumerate(versions):
        if min_max[0] <= version <= min_max[1]:
            return index
    raise ValueError("QR Code's version is too high or too low. QR Code version must be between 1-40")

def Get_Free_Bit_Space(version:int):
    blocks_per_side = 17 + 4 * version
    
    finder_patterns = 8 * 8 * 3

    version_infos = 0 if version <= 6 else 2 * 3 * 6

    alignment_patterns_amount = Get_Alignment_Patterns_Amount(version)
    alignment_patterns = alignment_patterns_amount ** 2 * 5 * 5 + (alignment_patterns_amount - 1) * 2 * 4 * 5 if alignment_patterns_amount != 0 else 0

    timing_patterns = 2 * (blocks_per_side - 2 * 8)

    return blocks_per_side ** 2 - finder_patterns - version_infos - alignment_patterns - timing_patterns - 31

number_of_data_bits = {
    "L": [0, 152, 272, 440, 640, 864, 1088, 1248, 1552, 1856, 2192, 2592, 2960, 3424, 3688, 4184, 4712, 5176, 5768, 6360, 6888, 7456, 8048, 8752, 9392, 10208, 10960, 11744, 12448, 13048, 13880, 14744, 15640, 16568, 17528, 18448, 19472, 20528, 21616, 22496, 23648],
    "M": [0, 128, 224, 352, 512, 688, 864, 992,   1232, 1456, 1728, 2032, 2320, 2672, 2920, 3320, 3624, 4056, 4504, 5016, 5352, 5712, 6256, 6880, 7312, 8000, 8496, 9024,     9544, 10136, 10984, 11640, 12328, 13048, 13800, 14496, 15312, 15936, 16816, 17728, 18672],
    "Q": [0, 104, 176, 272, 384, 496, 608, 704,    880, 1056, 1232, 1440, 1648, 1952, 2088, 2360, 2600, 2936, 3176, 3560, 3880, 4096, 4544, 4912, 5312, 5744, 6032, 6464,     6968, 7288, 7880, 8264,     8920, 9368, 9848, 10288, 10832, 11408, 12016, 12656, 13328],
    "H": [0, 72, 128, 208, 288, 368, 480, 528,     688, 800, 976, 1120, 1264, 1440, 1576, 1784, 2024,   2264, 2504, 2728, 3080, 3248, 3536, 3712, 4112, 4304, 4768, 5024,     5288, 5608, 5960, 6344,     6760, 7208, 7688, 7888, 8432, 8768, 9136, 9776, 10208],
}


class Error_Correction:
    def __init__(self):
        pass
        self.antilog_map = [0] * 256
        self.log_map = [0] * 256

        self.Generate_Antilog_Log_Maps()

        self.generated_polynomials = dict()


    def Generate_Error_Correction(self, encoded_text_in_decimal:list[int], qr_code_version:int, error_correction_level:str, error_correction_bytes_amount:int = None):
        if error_correction_bytes_amount is None:
            error_correction_bytes_amount = math.ceil((Get_Free_Bit_Space(qr_code_version) - number_of_data_bits[error_correction_level][qr_code_version]) / 8)

        root_generator_polynomial = self.Polynomial_Multiplication(error_correction_bytes_amount)
        message_polynomial = self.Polynomial_Multiplication(len(encoded_text_in_decimal) - 1)
        message_polynomial = [{"a": encoded_text_in_decimal[i], "x": value["x"]} for i, value in enumerate(message_polynomial)]

        message_polynomial = list(map(lambda x: {"a": x["a"], "x": x["x"] + 10}, message_polynomial))
        using_generator_polynomial = list(map(lambda x: {"a": x["a"], "x": x["x"] + 15}, deepcopy(root_generator_polynomial)))

        xor_polynomial = deepcopy(message_polynomial)

        for _ in range(len(message_polynomial)):

            #Get first term in the root generator polynomial
            lead_term_of_xor_polynomial = self.log_map[xor_polynomial[0]["a"]]

            #Multiply exponents together and mod the value
            using_generator_polynomial = list(map(lambda x: {"a": self.antilog_map[(x["a"] + lead_term_of_xor_polynomial) % 255], "x": x["x"]}, root_generator_polynomial))
            
            #Add extra values to the using polynomial in case its smaller than the using generator polynomial
            if len(using_generator_polynomial) > len(xor_polynomial):
                for i in range(len(using_generator_polynomial) - len(xor_polynomial)):
                    xor_polynomial.append({"a": 0, "x": xor_polynomial[-1]["x"] - 1})

            #XOR values from using polynomial and generator polynomial
            for i in range(len(xor_polynomial)):
                gen_value = using_generator_polynomial[i]["a"] if i < len(using_generator_polynomial) else 0

                xor_polynomial[i]["a"] = xor_polynomial[i]["a"] ^ gen_value
            
            #Remove any alpha values that are zero
            if xor_polynomial[0]["a"] == 0:
                xor_polynomial = xor_polynomial[1:]

        return [x['a'] for x in xor_polynomial]


    def Generate_Antilog_Log_Maps(self):
        self.antilog_map[0] = 1

        for i in range(1, 256):
            self.antilog_map[i] = self.antilog_map[i - 1] * 2
            
            if self.antilog_map[i] >= 256:
                self.antilog_map[i] ^= primitive_polynomial
            
            self.log_map[self.antilog_map[i]] = i

        self.log_map.remove(255)
        self.log_map.insert(0, 0)
    

    def Repair_Exponent(self, exponent:int):
        if exponent >= 256:
            return exponent % 256 + exponent // 256
        return exponent


    def Polynomial_Multiplication(self, amount_of_ec_codewords:int):
        if amount_of_ec_codewords in self.generated_polynomials.keys():
            return deepcopy(self.generated_polynomials[amount_of_ec_codewords])
        
        first_polynomial = [{"a": 0, "x": 1}, {"a": 0, "x": 0}]
        second_polynomial = [{"a": 0, "x": 1}, {"a": 1, "x": 0}]


        for _ in range(1, amount_of_ec_codewords):
            temp_return_polynomial = []

            for vars1 in first_polynomial:
                for vars2 in second_polynomial:
                    new_value = {"a": (vars1["a"] + vars2["a"]) % 255, "x": vars1["x"] + vars2["x"]}

                    for existing_value in temp_return_polynomial:
                        if new_value["x"] == existing_value["x"]:
                            new_value["a"] = self.Repair_Exponent(self.log_map[self.antilog_map[new_value["a"]] ^ self.antilog_map[existing_value["a"]]])

                            temp_return_polynomial.remove(existing_value)
                            break
                            
                    temp_return_polynomial.append(new_value)

            first_polynomial = deepcopy(temp_return_polynomial)
            second_polynomial[1]["a"] += 1
        
        final_polynomial = sorted(deepcopy(temp_return_polynomial), key=lambda x: x["x"], reverse=True)
        self.generated_polynomials[amount_of_ec_codewords] = deepcopy(final_polynomial)
        
        return final_polynomial

if __name__ == "__main__":
    ec = Error_Correction()
    print(ec.Generate_Error_Correction([67,85,70,134,87,38,85,194,119,50,6,18,6,103,38], 1, "M", 18))