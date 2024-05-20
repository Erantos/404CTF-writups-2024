from Crypto.Util.number import *
from tqdm import tqdm

def split(f):
        if len(f) & 1:
            f += b"\x00"
        h = len(f) // 2
        return (bytes_to_long(f[:h]), bytes_to_long(f[h:]))

with open("out.txt") as f:
    p = int(f.readline().replace('\n', ''))
    xf, yf = [int(i) for i in f.readline().replace('\n', '')[1:][:-1].split(',')]
    k, xn, yn = [int(i) for i in f.readline().replace('\n', '')[1:][:-1].split(',')]


# Finding (a^2+b^2) ^ (k/2)
clear_msg = b"L'eau est vraiment froide par ici (et pas tres propre)"

x0, y0 = split(clear_msg)
n = k/2

R = IntegerModRing(p)

xn, yn = R(xn), R(yn)
x0, y0 = R(x0), R(y0)
q = xn / x0

# Finding a^2 + b^2
a2_b2 = q.nth_root(n)
a, b = var("a b")
assume(a, 'integer')
assume(b, 'integer')

all_sols = solve([a^2 + b^2 == int(a2_b2)], a, b)
pos_sols = [sol for sol in all_sols if sol[0] > 0 and sol[1] > 0]

clear = b'404CTF{'
a2_b2_inv = pow(a2_b2, -1, p)
a2_b2_inv_n = pow(a2_b2_inv, n, p)

# Bruteforce sols (64 possibilites)
def bruteforce_sols(sols, known, xn, yn):
    for a,b in tqdm(sols):
        xf_1, yf_1 = xn, yn
        a,b = int(a), int(b)
        xf_1 = (a*xf + b*yf) % p
        yf_1 = (b*xn - a*yn) % p
        for i in range(2**19):
            xf_1 = (xf_1 * a2_b2_inv)  % p
            yf_1 = (yf_1 * a2_b2_inv) % p
            msg = long_to_bytes(int(xf_1)) + long_to_bytes(int(yf_1))
            if (known in msg):
                print("Found k=", i)
                return msg
    return b'Nothing found...'
            
msg = bruteforce_sols(pos_sols, clear, xf, yf)
    
print(msg.decode())
             
