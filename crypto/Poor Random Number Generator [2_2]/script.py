from z3 import *
from LFSR import LFSR
from generator import CombinerGenerator

def to_8bits(n):
    b = bin(n)[2:]
    if len(b) == 8:
        return b
    b = '0'*(8-(len(b)%8))+b
    return b

# Extract known part of the key

with open('flag.png.enc', 'rb') as f:
    flag_enc = f.read()

with open('flag.png.part', 'rb') as f:
    flag_part = f.read()

AVAILABLE_BYTES = len(flag_part)
TOT_LENGTH = AVAILABLE_BYTES * 8
POLY_LENGTH = 19

flag_enc = flag_enc[:AVAILABLE_BYTES]
key = "".join([to_8bits(a^b) for a,b in zip(flag_enc, flag_part)])
key_bool = [c == '1' for c in key]

# Z3 part

s1 = [Bool('s1_%s' % i) for i in range(TOT_LENGTH)]
s2 = [Bool('s2_%s' % i) for i in range(TOT_LENGTH)]
s3 = [Bool('s3_%s' % i) for i in range(TOT_LENGTH)]

# combine() function
f_cons = [Xor(And(s1[i], s2[i]), Xor(And(s1[i], s3[i]), And(s2[i], s3[i]))) == key_bool[i] for i in range(TOT_LENGTH)]

# Polynome constraints
s1_cons = [s1[i] == Xor(s1[i-19], Xor(s1[i-5], Xor(s1[i-2], s1[i-1]))) for i in range(POLY_LENGTH, TOT_LENGTH)]
s2_cons = [s2[i] == Xor(s2[i-19], Xor(s2[i-6], Xor(s2[i-2], s2[i-1]))) for i in range(POLY_LENGTH, TOT_LENGTH)]
s3_cons = [s3[i] == Xor(s3[i-19], Xor(s3[i-9], Xor(s3[i-8], s3[i-5]))) for i in range(POLY_LENGTH, TOT_LENGTH)]

s = Solver()
s.add(f_cons)
s.add(s1_cons)
s.add(s2_cons)
s.add(s3_cons)

print(s.check())

# Get initial state from model
m = s.model()
state1 = [1 if m[s] == True else 0 for s in s1[:19]][::-1]
state2 = [1 if m[s] == True else 0 for s in s2[:19]][::-1]
state3 = [1 if m[s] == True else 0 for s in s3[:19]][::-1]

poly1 = [19,5,2,1]
poly2 = [19,6,2,1]
poly3 = [19,9,8,5]

# Generate key as in encrypt.py
def xor(b1, b2):
	return bytes(a ^ b for a, b in zip(b1, b2))

combine = lambda x1,x2,x3 : (x1 and x2)^(x1 and x3)^(x2 and x3)

L1 = LFSR(fpoly=poly1,state=state1)
L2 = LFSR(fpoly=poly2,state=state2)
L3 = LFSR(fpoly=poly3,state=state3)

generator = CombinerGenerator(combine,L1,L2,L3)

# Decode flag
encrypted_flag = None
with open("flag.png.enc","rb") as f:
	encrypted_flag = f.read()

clear_flag = b''
for i in range(len(encrypted_flag)):
	random = generator.generateByte()
	byte = encrypted_flag[i:i+1]
	clear_flag += xor(byte,random)

with open("flag.png","w+b") as f:
	f.write(clear_flag)



