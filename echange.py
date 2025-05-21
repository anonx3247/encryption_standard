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
    I = internal_secret * G
    #LOOK INTO MAYBE ADDING SOMETHING ELSE HERE

    sig = sign(my_sign_secret_key, ZZ(I[0])) #sign x coord only
    msg1 = (I, sig)

    return internal_secret, msg1

def akex_final(other_sign_public_key, internal_secret, msg2):

    J, sig = msg2
    #to turn the point in the curb into a hashable message we make m the concatenation of x and y coords.
    #m = (ZZ(J[0]) >> 128) | ZZ(J[1]) #concat...
    if not verify(public_key = other_sign_public_key, signature = sig, m = ZZ(J[0])):
        raise Exception('Signature verification failed')
    
    shared = internal_secret * J

    #LOOK INTO ADDING SOMETHING ELSE HERE
    h = ZZ(hash(shared[0]))

    key1 = (h >> 64) & (2 ** 64 - 1) # get the first 64 bits after hash (-> 128 bits). Maybe actually just use h[0:63]
    key2 = h & (2**64 - 1) # get the second 64 bits of the key after hash (-> 128 bits) Maybe actually just use h[64:128]

    shared_keys = [key1, key2]

    return shared_keys

if __name__ == '__main__':

    privA, pubA = signature_keygen()
    privB, pubB = signature_keygen()

    #alice sends signed message (A)
    a, msg1 = akex_init(privA)

    #bob sends signed message (B)
    b, msg2 = akex_init(privB)

    #now alice checks Bob is who he says he is before checking the key
    shared_keys_a = akex_final(msg2[0], a, msg2) #might be something wrong? But from what I understand the public key is A for alice, B for Bob

    #so will alice
    shared_keys_b = akex_final(msg1[0], b, msg1)

    print(f'{shared_keys_a}\n{shared_keys_b}') 

    #to check if it can go wrong but it still works??
    #bad_sig_B = (sig_B[0] + 1, sig_B[1])
