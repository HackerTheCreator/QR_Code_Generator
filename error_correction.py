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


class Error_Correction:
    def __init__(self):
        pass
        self.antilog_map = [0] * 256
        self.log_map = [0] * 256

        self.Generate_Antilog_Log_Maps


    def Generate_Error_Correction(self, encoded_text_in_decimals:list[int]):
        error_correction_bytes_amount = math.ceil((Get_Free_Bit_Space(qr_code_version) - number_of_data_bits[error_correction_level][qr_code_version]) / 8)

        root_generator_polynomial = self.Polynomial_Multiplication(error_correction_bytes_amount)
        message_polynomial = self.Polynomial_Multiplication(len(encoded_text_in_decimal) - 1)
        message_polynomial = list(map(lambda x: {"a" : encoded_text_in_decimal[message_polynomial.index(x)], "x" : x["x"]}, message_polynomial))

        message_polynomial = list(map(lambda x: {"a": x["a"], "x": x["x"] + 10}, message_polynomial))
        using_generator_polynomial = list(map(lambda x: {"a": x["a"], "x": x["x"] + 15}, deepcopy(root_generator_polynomial)))

        xor_polynomial = deepcopy(message_polynomial)



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
        
        return sorted(deepcopy(temp_return_polynomial), key=lambda x: x["x"], reverse=True)
