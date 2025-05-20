import numpy as np

def block_encrypt(k: np.uint16, m: int) -> int:
    # separate into 64-bit blocks with padding
    m_blocks = [m[i:i+64] for i in range(0, len(m), 64)]
    
    

def block_decrypt(k: np.uint16, c: int) -> int:
    
