cipher = "C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o"
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"

beginFlag = "404CTF{tHe_c"

n = len(charset)
R = IntegerModRing(n)


x0_s = [R(charset.index(beginFlag[i])) for i in range(6)]
x1_s = [R(charset.index(beginFlag[6+i])) for i in range(6) ] 
y0_s = [R(charset.index(cipher[i])) for i in range(6)]
y1_s = [R(charset.index(cipher[6+i])) for i in range(6)]

a_s = [(y1_s[i] - y0_s[i]) / (x1_s[i] - x0_s[i]) for i in range(6)]
b_s = [y0_s[i] - a_s[i] * x0_s[i] for i in range(6)]

flag = ""
for i, c in enumerate(cipher):
    y = charset.index(c)
    k = i % 6
    x = (y - b_s[k]) / a_s[k]
    flag += charset[x]

print(flag)