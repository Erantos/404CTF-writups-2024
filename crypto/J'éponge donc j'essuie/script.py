from pwn import *

context.log_level = "debug"

r = remote("challenges.404ctf.fr", 31952)

r.recvuntil(b"of hash : ")
hash = r.recvline().decode()[:-1]
r.recvuntil(b"> ")

hash = "10" + hash + "10"
hash = "0" * (512 - len(hash)) + hash

r.sendline(hash.encode())

r.recvall(timeout=2)
r.close()

