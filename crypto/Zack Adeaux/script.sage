from pwn import *
import zlib
import base64
import json

def decodeData(data):
    data = base64.b64decode(data)
    data = zlib.decompress(data).decode()
    data = json.loads(data)
    return data

def bitToBytes(bs):
    ocs = [bs[i:i+8] for i in range(0, len(bs), 8)]
    res = b''
    for o in ocs:
        res += int("".join(o),2).to_bytes(1, 'big')
    return res

r = remote("challenges.404ctf.fr", 31777)

r.recvline() # Intro text
data = r.recvline().decode()

parsed_data = decodeData(data)
pub_key = parsed_data['public_key']
enc_msg = parsed_data['encrypted']

r.close()

#### LLL attack

def getMinC(n, S):
    num = pow(n+1, n/2)
    den = pow(2, n*(n-1)/4) * S
    return ceil(num / den)

def getSol(Y, n):
    for i in range(n+1):
        if Y[i, n] == 0:
            for j in range(n+1):
                if abs(Y[i,j]) >  1:
                    break
                if j == n:
                    return Y[i]

n = len(pub_key)
C = getMinC(n, enc_msg)

base_b = [[1 if i == j else 0 for i in range(n+1)] for j in range(n)]
B = base_b + [[ei*C for ei in pub_key] + [-enc_msg*C]]

M = matrix(B).T
print("Start LLL")
Y = M.LLL()

sol = getSol(Y, n)
flag = bitToBytes(['0', '0'] + list(map(lambda x: str(x), sol)))
print(flag)

