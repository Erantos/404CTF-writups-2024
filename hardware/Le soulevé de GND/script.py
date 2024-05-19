data = [78,114,87,9,245,67,252,90,90,126,120,109,133,78,206,121,52,115,123,102,164,194,170,123,5,]

state = 0
A = 7
B = 1918273
N = 25

password = ""

for i in range(N):
    password += chr(data[i] ^ state)
    state = (A * state + B) % 256

print(f"404CTF{{{password}}}")