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
    return ZZ.random_element(1, p)

def signature_keygen():
    secret_key = secrandom(q)
    public_key = secret_key * G
    return secret_key, public_key

def sign(secret_key, m) :
    e = hash(m) % q
    k = secrandom(q)
    r = ZZ((k * G)[1]) % q
    s = ZZ(e * secret_key * r) * inverse_mod(k, q) % q
    sigma = (r, s)
    return sigma

def verify(public_key, signature, m) :
    r, s = signature
    t = inverse_mod(s, q) % q
    e = hash(m)
    u = r * e * t % q
    r_prime = u * public_key
    print("r = ", r)
    print("r_prime =", r_prime[1])
    success = r == r_prime[1]
    return success


m = 0b10010010100010101010101001

priv, pub = signature_keygen()

signature = sign(priv, m)
ver = verify(pub, signature, m)
print(ver)