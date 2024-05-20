from Crypto.Util.number import long_to_bytes
from tqdm import tqdm

with open("flag.png.enc", "rb") as f:
    cipher = f.read()

with open("flag.png.part", "rb") as f:
    part_clear = f.read()

init_state_gen = [cipher[i] ^ part_clear[i] for i in range(2000)]
feed = init_state_gen

def get_next_byte(feed):
    number = 0

    for i in range(len(feed)):
        if i%2==0:
            number += pow(feed[i],i,2**8) + feed[i]*i
            number = ~number
        else:
            number ^= feed[i]*i+i


    number %= 2**8
    feed = feed[1:]
    feed.append(number)
    return number, feed

gen_numbers = []
for i in tqdm(range(len(cipher) - len(part_clear))):
    n, feed = get_next_byte(feed)
    gen_numbers.append(n)

key = init_state_gen + gen_numbers
flag = b"".join([long_to_bytes(cipher[i] ^ b) for i,b in enumerate(key)])

with open("flag.png", "wb") as f:
    f.write(flag)