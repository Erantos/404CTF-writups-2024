cipher = "-4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_"
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"

n = len(charset)
R = IntegerModRing(n)

x0 = R(charset.index('4'))
x1 = R(charset.index('0'))
y0 = R(charset.index(cipher[0]))
y1 = R(charset.index(cipher[1]))

a = (y1 - y0) / (x1 - x0)
b = y0 - a * x0

flag = ""
for c in cipher:
    y = charset.index(c)
    x = (y - b) / a
    flag += charset[x]

print(flag)