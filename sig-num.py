from sage.all import *
#from hash import hash

#can't access hash...
def hash(x): #change to actual hash function
    return x

def secrandom(n): # imagine this is the quality rng
    r  = randint(1, 2**n) # change the 0 for 2 ** (n - 1) if we don't count leading 0s as bits
    return r

'''
#to change later, using a curve of prime order found in the paper
p = 123456789012345678901234567890654833374525085966737125236501
a = 112507913528623610837613885503682230698868883572599681384335
b = -a
'''
#to change later. this is only a small curve for testing

p = 127
a = 1
b = 7
Fp = GF(p)
E = EllipticCurve(Fp, [0, 0, 0, a, b])
N = E.order()
G = E.gens()[0] # as a curve of prime order, any generator works

def signature_keygen():
    secret_key = secrandom(N)
    public_key = secret_key * G
    return secret_key, public_key

def sign(secret_key, m):
    e = hash(m)
    k = secrandom(N)
    r = (k * G)[0]
    s = (e + r*secret_key)*(inverse_mod(k, N))
    sigma = (r, s)
    return sigma

def verify(public_key, m, sigma):
    e = hash(m)
    t = Integer(sigma[1]).inverse_mod(Integer(N))
    r_prime = ((e*t)*G + (sigma[0]*t)*public_key)[0]

    success = Integer(r_prime) == Integer(sigma[0])

    return success

m = 0b1001001010

priv, pub = signature_keygen()

signature = sign(priv, m)
ver = verify(pub, m, signature)
print(ver)