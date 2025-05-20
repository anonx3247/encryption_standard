from bloc import block_encrypt, block_decrypt
from hash16 import hash
import numpy as np

def encrypt_and_authenticate(keys, m, aux=None):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    
    if aux is None:
        #aux = np.random.randint(0, 2**64, dtype=np.uint64)
        raise ValueError("No password")

    # Vérification que le nonce est sur 64 bits
    if aux >= 2**64:
        raise ValueError("Le nonce doit être sur 64 bits")
    
    # Chiffrement du message
    c = block_encrypt(k1, m)
    
    # Calcul du tag d'authentification
    auth_data = (c << 64) | aux
    #autre option : auth_data = (m << 128) | (c << 64) | aux

    tag = hash(auth_data) & 0xFFFFFFFFFFFFFFFF
    
    return aux, c, tag

def decrypt_and_verify(keys, aux, c, tag):
    if len(keys) != 2:
        raise ValueError("Deux clés sont requises")
    
    k1, k2 = keys
    
    # Vérification du tag avant déchiffrement
    auth_data = (c << 64) | aux
    computed_tag = hash(auth_data) & 0xFFFFFFFFFFFFFFFF
    
    if computed_tag != tag:
        return False, None
    
    # Déchiffrement du message seulement si le tag est valide
    m = block_decrypt(k2, c)
    
    return True, m
