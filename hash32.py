from sbox import sbox
import numpy as np

def chunk_binary(string, length):
    return [int(string[i:length+i].zfill(length), 2) for i in range(0, len(string), length)]

def p_128(value: int) -> int:
    # On extrait 4 blocs de 32 bits
    blocs = [(value >> (96 - 32*i)) & 0xFFFFFFFF for i in range(4)]
    # On applique la S-box 32 bits sur chaque bloc
    blocs = [sbox(b) for b in blocs]
    # On recompose le mot 128 bits
    return sum([blocs[i] << (96 - 32*i) for i in range(4)])

def hash(message : int) -> int :
    """
    Calcule le hash d'un message de taille quelconque, selon la construction de Merkle–Damgård.
    Pour la fonction, nous utilisons une construction du type Davies–Meyer, avec la 
    fonction f(M, S) = sbox(M ^ S) ^ S
    Le S initial est un entier de 128 bits généré aléatoirement.
    """
    chunk_size = 128

    binary_message = bin(message)[2:]
    message_chunks = chunk_binary(binary_message, chunk_size)

    state = 0b11110001111110010101001100011001111010101010101011111010110111001101010100011000111010111111010100000111010100111011010111100011

    for chunk in message_chunks :
        state = p_128(chunk ^ state) ^ state

    return state

for i in [2**75, 2**75+1] : # range(100, 110) :
    print(f"Valeur de la sbox pour {i} : {hex(hash(i))}")
