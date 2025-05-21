from sbox import sbox
import numpy as np
from bloc import split_blocks_128

def chunk_binary(message):
    return split_blocks_128(message)

def p_128(value: int) -> int:
    # 128 bits divisés en 8 blocs de 16 bits
    blocs = [(value >> (128 - 16*(i+1))) & 0xFFFF for i in range(8)]
    blocs = [sbox(np.uint16(b)) for b in blocs]
    blocs = [int(blocs[i]) << (128 - 16*(i+1)) for i in range(8)]
    return sum(blocs)

def hash(message: int) -> int:
    """
    Merkle–Damgård avec f(M, S) = p_128(M ^ S) ^ S
    """
    message_chunks = chunk_binary(message)

    state = 0b11110001111110010101001100011001111010101010101011111010110111001101010100011000111010111111010100000111010100111011010111100011

    rounds = 256
    for _ in range(rounds):
        for chunk in message_chunks:
            state = p_128(chunk ^ state) ^ state

    return state
