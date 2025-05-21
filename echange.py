from sage.all import *
from signature_sage import signature_keygen, sign, verify
from hash16 import hash

p = 2**128 + 51

a = 2
b = 36
K = GF(p)

E = EllipticCurve(K, [0, 0, 0, a, b])
G = E.gens()[0]
N = E.order()

def akex_init(my_sign_secret_key, my_sign_public_key = None): # why public key here??
    
    internal_secret = ZZ.random_element(1, N) 
    K_i = internal_secret * G
    sig = sign(my_sign_secret_key, K_i[0])
    msg1 = (K_i, sig)

    return internal_secret, msg1

def akex_final(other_sign_public_key, internal_secret, msg2):

    B, sig = msg2
    if not verify(other_sign_public_key, sig, B[0]):
        raise Exception('Signature verification failed')
    
    shared = internal_secret * B
    h = ZZ(hash(shared[0]))

    key1 = (h >> 64) & (2 ** 64 - 1) # get the first 64 bits after hash (-> 128 bits)
    key2 = h & (2**64 - 1) # get the second 64 bits of the key after hash (-> 128 bits)

    shared_keys = [key1, key2]

    return shared_keys

if __name__ == '__main__':

    privA, pubA = signature_keygen()
    privB, pubB = signature_keygen()

    a, msg1 = akex_init(privA)

    b = ZZ.random_element(1, N)
    B = b * G
    sig_B = sign(privB, B[0])
    #to check if it can go wrong but it still works??
    bad_sig_B = (sig_B[0] + 1, sig_B[1])

    msg2 = (B, sig_B)

    shared_keys = akex_final(pubB, a, msg2)
    print(f'shared: {shared_keys}')