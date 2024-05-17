def to_8bits(n):
    b = bin(n)[2:]
    if len(b) == 8:
        return b
    b = '0'*(8-(len(b)%8))+b
    return b

with open("challenge.txt", 'rb') as f:
    challenge = f.read()

with open("mobydick.txt", 'rb') as f:
    mobydick = f.read()

xor_diffs_tot = [to_8bits(a ^ b) for a, b in zip(mobydick, challenge)]
xor_diffs_bytes_tot = [int(i,2).to_bytes(1, 'big') for i in xor_diffs_tot]

res = b''
for i in range(150, len(xor_diffs_bytes_tot), 30):
    res += xor_diffs_bytes_tot[i]

with open("flag.png", "wb") as f:
    f.write(res)

