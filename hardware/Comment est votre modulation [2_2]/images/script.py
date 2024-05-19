import matplotlib.pyplot as plt
import numpy as np

F_C = 7e3
F_E = int(50*F_C)
T_E = 1/F_E
R = 1000 
T = 1/R
NB_SOUS_PORTEUSES = 8

data = np.fromfile("flag.iq", dtype='complex64')

# Demodulate OFDM
bits = []
for i in range(0, len(data), 350):
    part_data = data[i:i+350]
    for k in range(NB_SOUS_PORTEUSES):
        carry = [np.exp(-2j*np.pi*k*t*T_E/T) for t in range(int(F_E*T))]
        m = np.round(np.mean(part_data * carry))
        bits.append(m)
        part_data -= [m * c for c in carry]

# Decode QAM16
def unQAM(c):
    r = (c.real + 3) // 2
    im = (c.imag - 3) // -2
    return int(4*r+im)

res = b''
for i in range(0, len(bits), 2):
    b1, b2 = unQAM(bits[i]), unQAM(bits[i+1])
    res += int.to_bytes(b1*16+b2, 1, 'big')

with open("flag.png", "wb") as f:
    f.write(res)