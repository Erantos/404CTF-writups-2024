import struct
from math import floor
import matplotlib.pyplot as plt

with open("flag.raw", 'rb') as f:
    data = f.read()

# Parse raw bytes as 4-bytes float
data_f = [struct.unpack('f', data[i:i+4])[0] for i in range(0, len(data), 4)] 

# Plot signal on 6 symbols
n = 6
x = [i for i in range(350 * n)]
y = data_f[:n*350]
plt.plot(x, y)
plt.show()


syms = [floor(data_f[i] * 256) for i in range(0,len(data_f), 350)] # 256 uniq values between 0 and 256 (255 is missing)
syms = [255 if s == 256 else s for s in syms]
bsyms = [s.to_bytes(1, 'big') for s in syms]

with open('flag.png', 'wb') as f:
    for b in bsyms:
        f.write(b)