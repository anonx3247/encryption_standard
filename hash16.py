from sbox import sbox
import numpy as np

def chunk_binary(string, length):
    return [int(string[i:i+length].zfill(length), 2) for i in range(0, len(string), length)]

def p_128(value: int) -> int:
    # 128 bits divisés en 8 blocs de 16 bits
    blocs = [(value >> (112 - 16*i)) & 0xFFFF for i in range(8)]
    blocs = [sbox(np.uint16(b)) for b in blocs]
    return sum([int(blocs[i] << (112 - 16*i)) for i in range(8)])

def hash(message: int) -> int:
    """
    Merkle–Damgård avec f(M, S) = p_128(M ^ S) ^ S
    """
    chunk_size = 128
    binary_message = bin(message)[2:]
    message_chunks = chunk_binary(binary_message, chunk_size)

    state = 0b11110001111110010101001100011001111010101010101011111010110111001101010100011000111010111111010100000111010100111011010111100011


    for chunk in message_chunks:
        state = p_128(chunk ^ state) ^ state

    return state

# Test
for i in [2**75, 2**75 + 1]:
    print(f"Valeur de la sbox pour {i} : {hex(hash(i))}")

