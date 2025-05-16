from sbox import sbox
import numpy as np

def chunk_binary(string, length):
    return [int(string[i:length+i].zfill(length), 2) for i in range(0, len(string), length)]

def p_128(value : int) -> int :
    gauche = int(sbox((value >> 64) & 0xFFFFFFFFFFFFFFFF))
    droite = int(sbox(value & 0xFFFFFFFFFFFFFFFF))
    return gauche << 64 | droite

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
    # print(len(bin(state)) - 2)
    
    for chunk in message_chunks :
            state = p_128(chunk ^ state) ^ state

    return state

for i in [2**75, 2**75+1] : # range(100, 110) :
    print(f"Valeur de la sbox pour {i} : {hex(hash(i))}")