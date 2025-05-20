from bloc import block_encrypt, block_decrypt
from hash16 import hash
import numpy as np

def encrypt_and_authenticate(keys: list[np.uint16], m: int, aux=None):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    
    # Chiffrement du message
    c = block_encrypt(k1, m)

    tag = hash(m ^ k2)
    
    return aux, c, tag

def decrypt_and_verify(keys: list[np.uint16], c: int, tag: int):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    
    # Vérification du tag avant déchiffrement
    computed_tag = hash(m ^ k2)
    
    if computed_tag != tag:
        return False, None
    
    # Déchiffrement du message seulement si le tag est valide
    m = block_decrypt(k1, c)
    
    return True, m
