from sbox import sbox
import numpy as np
import random as rd

def chunk_binary_md(string: str, length: int) -> list[int]:
    """
    Cette fonction propose un padding MD-compliant, pour garantir la sécurité
    des messages même à petite taille. Elle est inspirée de la version originale
    proposée par la version originale, mais ajoute à la fin les 32 bits de poids fort
    du message original.
    """
    padded = string + '1'
    
    # On ajoute des 0 jusqu'à ce que padded + 32 soit de taille multiple de length
    total_len = len(padded) + 32
    pad_len = (length - (total_len % length)) % length
    padded += '0' * pad_len

    # On ajoute les 32 bits de poids fort du message original
    padded += f"{int(string, 2):032b}"

    # On divise le message en morceaux de taille length
    return [int(padded[i:i+length], 2) for i in range(0, len(padded), length)]

def p_128(value: int) -> int:
    # 128 bits divisés en 8 blocs de 16 bits
    blocs = [(value >> (128 - 16*(i+1))) & 0xFFFF for i in range(8)]
    blocs = [sbox(np.uint16(b)) for b in blocs]
    blocs = [int(blocs[i]) << (128 - 16*(i+1)) for i in range(8)]
    return sum(blocs)

def hash(message: int) -> int:
    """
    Hybride entre éponge et Merkle–Damgård avec f(M, S) = p_128(M ^ S) ^ S
    """
    chunk_size = 128
    binary_message = bin(message)[2:]
    message_chunks = chunk_binary_md(binary_message, chunk_size)

    n = len(message_chunks)
    c = 128 // n
    c_left = 128 % n

    result = 0

    state = 0b11110001111110010101001100011001111010101010101011111010110111001101010100011000111010111111010100000111010100111011010111100011
    bit_pos = 128

    for i in range(n) :
        chunk = message_chunks[i]
        state = p_128(chunk ^ state) ^ state

        size = c + c_left if i == n - 1 else c
        bit_pos -= size

        # On extrait les 'size' bits de state
        part = (state >> (128 - size)) & ((1 << size) - 1)

        # On ajoute ces bits à la position souhaitée
        result = result | (part << bit_pos)

    return result