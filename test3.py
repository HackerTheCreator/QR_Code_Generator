import copy

#Create log and antilog maps 
#Error with zero -> 255


primitive_polynomial = 0b100011101

antilog_map = [0] * 256
log_map = [0] * 256

def Generate_Antilog_Log_Maps():

    antilog_map[0] = 1
    for i in range(1, 256):
        antilog_map[i] = antilog_map[i - 1] * 2
        
        if antilog_map[i] >= 256:
            antilog_map[i] ^= primitive_polynomial
        
        log_map[antilog_map[i]] = i
    log_map.remove(255)
    log_map.insert(0, 0)


def Anti_Log(exponent:int)->int:
    new_number = 1

    for _ in range(exponent):
        new_number *= 2
        if new_number >= 256:
            new_number ^= primitive_polynomial
        
    return new_number


def Log(integer:int)->int:
    for i in range(256):
        if Anti_Log(i) == integer:
            return i
    raise ValueError(f"Set integer ({integer}) has not any log value to it.")


def Repair_Exponent(exponent:int):
    if exponent >= 256:
        return exponent % 256 + exponent // 256
    return exponent
    

def Polynomial_Multiplication(amount_of_ec_codewords:int):
    first_polynomial = [{"a": 0, "x": 1}, {"a": 0, "x": 0}]
    second_polynomial = [{"a": 0, "x": 1}, {"a": 1, "x": 0}]


    for _ in range(1, amount_of_ec_codewords):
        temp_return_polynomial = []

        for vars1 in first_polynomial:
            for vars2 in second_polynomial:
                new_value = {"a": (vars1["a"] + vars2["a"]) % 255, "x": vars1["x"] + vars2["x"]}

                for existing_value in temp_return_polynomial:
                    if new_value["x"] == existing_value["x"]:
                        new_value["a"] = Repair_Exponent(log_map[antilog_map[new_value["a"]] ^ antilog_map[existing_value["a"]]])

                        temp_return_polynomial.remove(existing_value)
                        break
                        
                temp_return_polynomial.append(new_value)

        first_polynomial = copy.deepcopy(temp_return_polynomial)
        second_polynomial[1]["a"] += 1
    
    return sorted(copy.deepcopy(temp_return_polynomial), key=lambda x: x["x"], reverse=True)

Generate_Antilog_Log_Maps()

