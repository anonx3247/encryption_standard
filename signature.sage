import random as rd
from hash16 import hash

p = 2^128 + 51
K = GF(p)

a = 2
b = 36

E = EllipticCurve(K, [a, b])

print(E.order() - 2^128)

G = E.gens()[0]
q = G.order()

print(G)

def secrandom(length) :
    return rd.randint(1, 2**length - 1)

def signature_keygen():
    secret_key = secrandom(q)
    public_key = secret_key * G
    return secret_key, public_key

def sign(secret_key, m) :
    e = hash(m)
    k = secrandom(q)
    r = (k * G)[1]
    s = (e * r * secret_key) * k.inverse() 
    sigma = (r, s)

def verify(public_key, signature, m) :
    r, s = signature
    t = inverse_mod(s, q)
    e = hash(m)
    r_prime = (e * r * t * public_key)[1]
    success = r == r_prime
    return success


m = 0b1001001010

priv, pub = signature_keygen()

signature = sign(priv, m)
ver = verify(pub, m, signature)
print(ver)