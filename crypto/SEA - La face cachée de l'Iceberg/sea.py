import os
from Crypto.Util.number import long_to_bytes,bytes_to_long
from hashlib import shake_256
SBOX_1=[
	0x24,0xc1,0x38,0x30,0xe7,0x57,0xdf,0x20,0x3e,0x99,0x1a,0x34,0xca,0xd6,0x52,0xfd,
	0x40,0x6c,0xd3,0x95,0x4a,0x59,0xf8,0x77,0x79,0x61,0x0a,0x56,0xb9,0xd2,0xfc,0xf1,
	0x07,0xf5,0x93,0xcd,0x00,0xb6,0xcb,0xa7,0x63,0x98,0x44,0xbd,0x5f,0x92,0x6b,0x73,
	0x3c,0x4e,0xa2,0x97,0x0b,0x01,0x83,0xa3,0xee,0xe5,0x45,0x67,0xf4,0x13,0xad,0x8b,
	0xbb,0x0c,0x72,0xb4,0x2a,0x3a,0xc5,0x84,0xec,0x9f,0x14,0xc0,0xc4,0x16,0x31,0xd9,
	0xab,0x9e,0x0e,0x1d,0x7c,0x48,0x1b,0x05,0x1c,0xea,0xa5,0xf0,0x8f,0x85,0x50,0x2c,
	0x35,0xbf,0x26,0x28,0x7b,0xe2,0xaa,0xf9,0x4f,0xe3,0xcc,0x2e,0x11,0x76,0xb1,0x8d,
	0xd4,0x5e,0xaf,0xe8,0x42,0xb0,0x6d,0x65,0x82,0x6a,0x58,0x8a,0xdd,0x7e,0x22,0xd8,
	0xe0,0x4c,0x2d,0xcf,0x75,0x12,0x8e,0xb2,0xbc,0x36,0x2b,0x25,0xe1,0x78,0xfa,0xa9,
	0x69,0x81,0x89,0x5b,0x7d,0xde,0xdb,0x21,0x5d,0xd7,0xeb,0xac,0xb3,0x41,0x66,0x6e,
	0x9c,0xef,0xc3,0x17,0x15,0xc7,0xda,0x32,0x0f,0xb8,0xb7,0x71,0x39,0x29,0x87,0xc6,
	0xe9,0x1f,0xf3,0xa6,0x86,0x8c,0x2f,0x53,0x9d,0xa8,0x1e,0x0d,0x4b,0x7f,0x06,0x18,
	0x9b,0x60,0xbe,0x47,0x91,0x5c,0x70,0x68,0xf6,0x04,0xce,0x90,0xb5,0x03,0xa4,0xc8,
	0xe6,0xed,0x64,0x46,0x10,0xf7,0x88,0xae,0x4d,0x3f,0x94,0xa1,0x02,0x08,0xa0,0x80,
	0x9a,0x3d,0x37,0x19,0xd5,0xc9,0xfe,0x51,0xc2,0x27,0x33,0x3b,0x54,0xe4,0x23,0xdc,
	0x62,0x7a,0x55,0x09,0xd1,0xba,0xf2,0xff,0x6f,0x43,0x96,0xd0,0x5a,0x49,0x74,0xfb,
]
SBOX_2=[
	0x24,0xc1,0x38,0x30,0xe7,0x57,0xdf,0x20,0x3e,0x99,0x1a,0x34,0xca,0xd6,0x52,0xfd,
	0x40,0x6c,0xd3,0x3d,0x4a,0x59,0xf8,0x77,0xfb,0x61,0x0a,0x56,0xb9,0xd2,0xfc,0xf1,
	0x07,0xf5,0x93,0xcd,0x00,0xb6,0x62,0xa7,0x63,0xfe,0x44,0xbd,0x5f,0x92,0x6b,0x68,
	0x03,0x4e,0xa2,0x97,0x0b,0x60,0x83,0xa3,0x02,0xe5,0x45,0x67,0xf4,0x13,0x08,0x8b,
	0x10,0xce,0xbe,0xb4,0x2a,0x3a,0x96,0x84,0xc8,0x9f,0x14,0xc0,0xc4,0x6f,0x31,0xd9,
	0xab,0xae,0x0e,0x64,0x7c,0xda,0x1b,0x05,0xa8,0x15,0xa5,0x90,0x94,0x85,0x71,0x2c,
	0x35,0x19,0x26,0x28,0x53,0xe2,0x7f,0x3b,0x2f,0xa9,0xcc,0x2e,0x11,0x76,0xed,0x4d,
	0x87,0x5e,0xc2,0xc7,0x80,0xb0,0x6d,0x17,0xb2,0xff,0xe4,0xb7,0x54,0x9d,0xb8,0x66,
	0x74,0x9c,0xdb,0x36,0x47,0x5d,0xde,0x70,0xd5,0x91,0xaa,0x3f,0xc9,0xd8,0xf3,0xf2,
	0x5b,0x89,0x2d,0x22,0x5c,0xe1,0x46,0x33,0xe6,0x09,0xbc,0xe8,0x81,0x7d,0xe9,0x49,
	0xe0,0xb1,0x32,0x37,0xea,0x5a,0xf6,0x27,0x58,0x69,0x8a,0x50,0xba,0xdd,0x51,0xf9,
	0x75,0xa1,0x78,0xd0,0x43,0xf7,0x25,0x7b,0x7e,0x1c,0xac,0xd4,0x9a,0x2b,0x42,0xe3,
	0x4b,0x01,0x72,0xd7,0x4c,0xfa,0xeb,0x73,0x48,0x8c,0x0c,0xf0,0x6a,0x23,0x41,0xec,
	0xb3,0xef,0x1d,0x12,0xbb,0x88,0x0d,0xc3,0x8d,0x4f,0x55,0x82,0xee,0xad,0x86,0x06,
	0xa0,0x95,0x65,0xbf,0x7a,0x39,0x98,0x04,0x9b,0x9e,0xa4,0xc6,0xcf,0x6e,0xdc,0xd1,
	0xcb,0x1f,0x8f,0x8e,0x3c,0x21,0xa6,0xb5,0x16,0xaf,0xc5,0x18,0x1e,0x0f,0x29,0x79,
]

class SEA:
	def __init__(self,SBox1,SBox2,key):
		self.ROUND_NB = 4
		self.BLOCK_SIZE = 16
		self.SBox1 = SBox1
		self.SBox2 = SBox2
		self.key = key
		self.round_keys = [bytes_to_long(self.key[:self.BLOCK_SIZE])]+self._key_expansion()
		self.state = None

	def pad(self,data):
		if len(data)%self.BLOCK_SIZE==0:
			return data
		return data+b'\x00'*(self.BLOCK_SIZE-(len(data)%self.BLOCK_SIZE))

	def _key_expansion(self):
		expanded = [shake_256(self.key[self.BLOCK_SIZE:]).digest(length=self.BLOCK_SIZE//2)]

		for i in range(self.ROUND_NB-1):
			expanded.append(shake_256(expanded[-1]).digest(length=self.BLOCK_SIZE//2))
		return [bytes_to_long(expanded[i]) for i in range(0,len(expanded))]

	def left_state(self):
		return self.state>>(self.BLOCK_SIZE*4)

	def right_state(self):
		return self.state&0xffffffffffffffff

	def apply_first_round(self):
		self.state = self.state^self.round_keys[0]

	def f(self,block):
		b1 = (block>>56)
		b2 = (block>>48) & 0xff
		b3 = (block>>40) & 0xff
		b4 = (block>>32) & 0xff
		b5 = (block>>24) & 0xff
		b6 = (block>>16) & 0xff
		b7 = (block>>8) & 0xff
		b8 = block & 0xff

		b2 ^= b3
		b1 ^= b2
		b1 = self.SBox1[b1]
		b2 ^= b1
		b2 = self.SBox2[b2]
		b3 ^= b2
		b3 = self.SBox2[b3]
		b3 ^= b1
		b4 ^= b5
		b4 = self.SBox2[b4]
		b5 ^= b4
		b5 = self.SBox1[b5]
		b7 ^= b6
		b6 = self.SBox1[b6]
		b7^= b6
		b7 = self.SBox2[b7]
		b8 ^= b7
		b6 ^= b7
		b8 = self.SBox1[b8]

		return (b2<<56)+(b3<<48)+(b6<<40)+(b1<<32)+(b4<<24)+(b8<<16)+(b5<<8)+b7

	def swap_state(self): #swap left half and right half of self.state
		left = self.left_state()
		right = self.right_state()
		self.state = (right<<self.BLOCK_SIZE*4)+left

	def apply_round(self,round_number):
		f_input = self.right_state()^self.round_keys[round_number]
		f_output = self.f(f_input)
		left = self.left_state()^f_output
		right = self.right_state()
		self.state = (left<<self.BLOCK_SIZE*4)+right

	def encrypt_block(self,block):
		states = []
		self.state = bytes_to_long(block)
		states.append(self.state)
		self.apply_first_round()
		for i in range(1,self.ROUND_NB+1):
			self.apply_round(i)
			self.swap_state()
			states.append(self.state)
		return long_to_bytes(self.state)

	def encrypt(self,data):
		blocks = [ self.pad(data[i:i+self.BLOCK_SIZE]) for i in range(0,len(data),self.BLOCK_SIZE) ]
		encrypted = b''
		for block in blocks:
			encrypted_b = self.encrypt_block(block)
			encrypted += encrypted_b
		return encrypted
from flag import FLAG

ENCRYPTION_NUMBER = 64
key = os.urandom(32)

cipher = SEA(SBOX_1,SBOX_2,key)
encrypted_flag = cipher.encrypt(FLAG)


print("""
	###############################
	 ____  _____    _    
	/ ___|| ____|  / \   
	\___ \|  _|   / _ \  
	 ___) | |___ / ___ \ 
	|____/|_____/_/   \_\\
		SillyEncryptionAlgorithm
	################################
	""")

print("I'm very lazy, I only accept blocks of 16 bytes at one time...")
print("Our encrypted secret :",encrypted_flag.hex())

while ENCRYPTION_NUMBER != 0:
	try:
		m = input("Send me something to encrypt (in hex format please) > ")
		if len(m) == 32:
			encrypted_m = cipher.encrypt(bytes.fromhex(m))
			print(encrypted_m.hex())
		elif len(m) > 32:
			print("Too loooooong !")
			exit()
		else:
			print("Too short !")
		ENCRYPTION_NUMBER -= 1
	except:
		print("Houston, we have a problem !")
		exit()

print("Enough encryptions, I'm tired !")