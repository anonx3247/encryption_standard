from bloc import block_encrypt, block_decrypt
from hash16 import hash
import numpy as np

def encrypt_and_authenticate(keys: list[np.uint16], m: int, aux=None):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    
    # Chiffrement du message
    c = block_encrypt(k1, m)

    k2 = int(k2)

    tag = hash(m ^ k2)
    
    return aux, c, tag

def decrypt_and_verify(keys: list[np.uint16], c: int, tag: int, aux=None):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    k2 = int(k2)
    
    # Déchiffrement du message seulement si le tag est valide
    m = block_decrypt(k1, c)

    
    # Vérification du tag avant déchiffrement
    computed_tag = hash(m ^ k2)
    
    if computed_tag != tag:
        return False, None
    
    return True, m
