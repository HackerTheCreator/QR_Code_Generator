import math

primitive_polynomial = 0b100011101

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

iterations = 255
for i in range(1, iterations + 1):
    print(Log(i))