from typing import List, Union


# Constants #
ADDITION_MODULO: int = 2 ** 32 # Modulo to perform addition in, defined in the specification sheet.
WORD_BITS: int = 32 # Bits of Words, defined in the specification sheet.

K: List[int] = [
    # Word Constants ~ Spec 4.2.2 #
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]


def encode(message: Union[str, bytes, bytearray]) -> str:
    message_arr: bytearray = message
    
    # Type Checking #
    if isinstance(message, str):
        message_arr = bytearray(message, "ascii")
    elif isinstance(message, bytes):
        message_arr = bytearray(message)
    elif not isinstance(message, bytearray):
        raise TypeError("Passed Message was not a valid type, type needs to be of 'str', 'bytes', or 'bytearray'.")
    
    
    # Padding ~ Spec 5.1.1 #
    message_length: int = len(message_arr) * 8
    message_arr.append(0x80)
    
    while (len(message_arr) * 8 + 64) % 512 != 0:
        message_arr.append(0x00)
    
    for b in message_length.to_bytes(8, "big"):
        message_arr.append(b)
    
    assert (len(message_arr) * 8) % 512 == 0, "Message could not be properly padded."
    
    
    # Parsing ~ Spec 5.2.1 #
    chunks: List[bytearray] = [  ]
    for i in range(0, len(message_arr), 64):
        chunks.append(message_arr[i : i + 64])
    
    
    # Set Intial Hash Values ~ Spec 5.3.2 #
    hash_table: List[int] = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]
    
    
    # Computation ~ Spec 6.2.2 #
    for c in chunks:
        w: List[int] = [  ]
        
        for t in range(0, 64):
            if t <= 15:
                w.append(c[t])
            else:
                w.append((lc_sigma_1(w[t - 2]) + w[t - 7] + lc_sigma_0(w[t - 15]) + w[t - 16]) % ADDITION_MODULO)
        
        assert len(w) == 64, "Could not properly created a message schedule."
        
        a = hash_table[0]
        b = hash_table[1]
        c = hash_table[2]
        d = hash_table[3]
        e = hash_table[4]
        f = hash_table[5]
        g = hash_table[6]
        h = hash_table[7]
        
        for t in range(0, 64):
            t1: int = (h + sigma_1(e) + ch(e, f, g) + K[t] + w[t]) % ADDITION_MODULO
            t2: int = (sigma_0(a) + maj(a, b, c)) % ADDITION_MODULO
            
            h, g, f = g, f, e
            e = (d + t1) % ADDITION_MODULO
            d, c, b = c, b, a
            a = (t1 + t2) % ADDITION_MODULO
        
        hash_table[0] = (a + hash_table[0]) % ADDITION_MODULO
        hash_table[1] = (b + hash_table[1]) % ADDITION_MODULO
        hash_table[2] = (c + hash_table[2]) % ADDITION_MODULO
        hash_table[3] = (d + hash_table[3]) % ADDITION_MODULO
        hash_table[4] = (e + hash_table[4]) % ADDITION_MODULO
        hash_table[5] = (f + hash_table[5]) % ADDITION_MODULO
        hash_table[6] = (g + hash_table[6]) % ADDITION_MODULO
        hash_table[7] = (h + hash_table[7]) % ADDITION_MODULO


# Helper Functions ~ Spec 4.1.2 #
rotate_right = lambda x, n : (x >> n) | (x << WORD_BITS - n)
rotate_left = lambda x, n : (x << n) | (x >> WORD_BITS - n)
ch = lambda x, y, z : (x & y) ^ (x & z)
maj = lambda x, y, z : (x & y) ^ (x & z) ^ (y & z)
sigma_0 = lambda x : rotate_right(x, 2) ^ rotate_right(x, 13) ^ rotate_right(x, 22)
sigma_1 = lambda x : rotate_right(x, 6) ^ rotate_right(x, 11) ^ rotate_right(x, 25)
lc_sigma_0 = lambda x : rotate_right(x, 7) ^ rotate_right(x, 18) ^ (x >> 3)
lc_sigma_1 = lambda x : rotate_right(x, 17) ^ rotate_right(x, 19) ^ (x >> 10)