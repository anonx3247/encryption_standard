from sbox import sbox

def chunk_binary(string, length, offset):
    return ["0" * (length - len(string[offset+i:offset+i+length])) + string[offset+i:offset+length+i] for i in range(0, len(string), length)]

def hash(m : int) -> int :
    part_size = 4

    binary_m = bin(m)[2:]
    messages = chunk_binary(binary_m, part_size, 2)

    return messages

print(hash(0x5A656))