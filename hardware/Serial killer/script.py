import numpy as np

bytes = np.fromfile("chall.bin", dtype = "uint8")
bits = np.unpackbits(bytes)

dataBits = [map(str, bits[i:i+7][::-1]) for i in range(1, len(bits), 10)]

flag = ""
for bs in dataBits:
    byte = int("".join(bs), 2)
    flag += chr(byte)

print(flag)