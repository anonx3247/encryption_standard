# Encryption Standard - Algebra & Cryptology Project

A comprehensive cryptographic system implementing custom encryption, hashing, digital signatures, and authenticated key exchange protocols.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Components](#components)
- [Usage Examples](#usage-examples)
- [Technical Details](#technical-details)
- [Requirements](#requirements)

## 🔍 Overview

This project implements a complete cryptographic protocol suite including:

1. **Block Cipher**: Custom 64-bit block cipher with S-box and linear diffusion layer
2. **Hash Function**: Sponge-Merkle–Damgård hybrid producing 128-bit hashes
3. **Authenticated Encryption**: Encrypt-then-MAC mode with authentication tags
4. **Digital Signatures**: Elliptic curve-based signature scheme
5. **Key Exchange**: Authenticated Key Exchange (AKEX) protocol using elliptic curves

## ✨ Features

- **Custom S-box Design**: 16-bit S-box with bit rotations and modular arithmetic
- **Linear Diffusion Layer**: 64-bit circulant matrix for optimal branch number
- **Authenticated Encryption**: Combined encryption and authentication using two keys
- **ECC-based Signatures**: Elliptic curve cryptography over GF(2^128 + 51)
- **Secure Key Exchange**: Authenticated key exchange with signature verification
- **Complete Protocol**: End-to-end secure communication with encryption and signatures

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- SageMath (for elliptic curve operations)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/anonx3247/encryption_standard
cd encryption_standard
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
encryption_standard/
├── main.py              # Main implementation with all protocols
├── encryption.py        # Block cipher implementation (modular)
├── sbox.py             # S-box functions
├── matrix_ops.py       # Matrix operations for linear layer
├── hash.py             # Hash function implementation
├── mode.py             # Authenticated encryption mode
├── echange.py          # Key exchange protocol
├── signature_sage.py   # Digital signature scheme
├── tests.py            # Unit tests and benchmarks
├── test.ipynb          # Jupyter notebook for testing
└── requirements.txt    # Python dependencies
```

## 🔧 Components

### 1. S-box (Substitution Box)

The S-box is a 16-bit non-linear transformation using:
- Bit rotations (5 and 7 positions)
- Affine transformations with constants
- Modular multiplication

**Operations**: `x → rotate → NOT(x ⊕ a) → multiply → NOT(x ⊕ b) → multiply → rotate`

### 2. Block Cipher

- **Block size**: 64 bits
- **Key size**: 64 bits
- **Rounds**: 16 (default)
- **Structure**: Substitution-Permutation Network (SPN)

**Each round**:
1. XOR with round key
2. Apply S-box to four 16-bit blocks
3. Apply linear diffusion layer (circulant matrix)

### 3. Hash Function

- **Output size**: 128 bits
- **Structure**: Hybrid sponge and Merkle–Damgård
- **Compression function**: `f(M, S) = p_128(M ⊕ S) ⊕ S`
- Divides input into 128-bit chunks and processes sequentially

### 4. Authenticated Encryption

**Mode**: Encrypt-then-MAC
- Uses two 64-bit keys (k1 for encryption, k2 for authentication)
- Tag computed as: `tag = hash(message ⊕ k2)`
- Verification before decryption (prevents padding oracle attacks)

### 5. Digital Signatures

**Elliptic Curve**: `y² = x³ + 2x + 36` over `GF(2^128 + 51)`

**Sign**: `(r, s)` where:
- `r = (k·G)_y mod q`
- `s = (e·sk·r) / k mod q`
- `e = hash(message) mod q`

**Verify**: Check if `r == (u·PK)_y` where `u = r·e·t mod q` and `t = 1/s mod q`

### 6. Authenticated Key Exchange (AKEX)

Protocol for establishing shared keys with mutual authentication:

1. **Alice**: Generates ephemeral key `a`, computes `I = a·G`, signs `I`, sends `(I, sig_A)`
2. **Bob**: Generates ephemeral key `b`, computes `J = b·G`, signs `J`, sends `(J, sig_B)`
3. **Both**: Verify signatures, compute shared secret `S = a·J = b·I`
4. **Derive**: Two 64-bit keys from `hash(S_x)` for authenticated encryption

## 💻 Usage Examples

### Basic Encryption/Decryption

```python
import numpy as np
from main import block_encrypt, block_decrypt

# Generate a 64-bit key
key = np.uint64(0x0123456789ABCDEF)

# Encrypt a message
message = 0x48656C6C6F576F726C64  # "HelloWorld" in hex
ciphertext, num_blocks = block_encrypt(key, message, rounds=16)

# Decrypt
plaintext = block_decrypt(key, ciphertext, rounds=16, num_blocks=num_blocks)
```

### Authenticated Encryption

```python
from main import encrypt_and_authenticate, decrypt_and_verify

# Two keys required
keys = [np.uint64(0x1234567890ABCDEF), np.uint64(0xFEDCBA0987654321)]

# Encrypt with authentication
message = 0x48656C6C6F
aux, cipher, tag = encrypt_and_authenticate(keys, message)

# Decrypt and verify
verified, decrypted = decrypt_and_verify(keys, cipher, tag, aux)
if verified:
    print(f"Message: {decrypted:x}")
```

### Digital Signatures

```python
from main import signature_keygen, sign, verify

# Generate key pair
secret_key, public_key = signature_keygen()

# Sign a message
message = 0x1234567890ABCDEF
signature = sign(secret_key, message)

# Verify signature
is_valid = verify(public_key, signature, message)
print(f"Signature valid: {is_valid}")
```

### Complete Protocol (Key Exchange + Encrypted Communication)

```python
from main import simulate_complete_protocol

# Simulates full protocol:
# 1. Key pair generation for Alice and Bob
# 2. Authenticated key exchange
# 3. Encrypted and signed message transmission
# 4. Decryption and signature verification
simulate_complete_protocol()
```

### Running Simulations

```python
from main import simulate_encryption, simulate_akex, simulate_signature

# Test encryption/decryption
simulate_encryption()

# Test key exchange protocol
simulate_akex()

# Test signature scheme
simulate_signature()
```

## 🔬 Technical Details

### S-box Parameters
- `a_sbox = 11109` (0x2B65)
- `b_sbox = 10403` (0x28A3)
- Bit rotations: 5 and 7 positions

### Linear Layer
- Circulant matrix from vector: `0xc063fe883bca8005`
- Provides optimal diffusion (maximizes differential branch number)
- Invertible for decryption

### Elliptic Curve Parameters
- Field: `p = 2^128 + 51`
- Curve: `y² = x³ + 2x + 36`
- Generator: `G` (first generator from SageMath)
- Order: `q = G.order()`

### Security Considerations

⚠️ **Educational Purpose**: This is an academic project for learning cryptography.

**Do NOT use in production**. This implementation:
- Has not undergone formal security analysis
- May contain implementation vulnerabilities
- Uses custom (non-standard) cryptographic primitives
- Is not optimized for side-channel resistance

For production systems, use established standards like AES, SHA-256, ECDSA, and TLS.

## 📦 Requirements

```
galois==0.4.6
llvmlite==0.44.0
numba==0.61.2
numpy==2.2.5
typing-extensions==4.13.2
```

Plus **SageMath** for elliptic curve operations.

## 🧪 Testing

Run the test suite:

```bash
python tests.py
```

Or use the Jupyter notebook for interactive testing:

```bash
jupyter notebook test.ipynb
```

## 📝 Notes

- All operations use little-endian byte order
- Messages are automatically padded to block boundaries
- Keys must be exactly 64 bits for encryption
- Signatures require both parties to exchange public keys securely beforehand

## 🎓 Academic Context

This project was developed as part of an **Algebra and Cryptology** course, demonstrating:
- Design and implementation of cryptographic primitives
- Security properties (confusion, diffusion)
- Protocol composition
- Mathematical foundations (finite fields, elliptic curves)

---

**Author**: Exam Project  
**Course**: Algèbre et Cryptologie  
**Language**: Python 3 + SageMath
