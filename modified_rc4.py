import struct
from pathlib import Path

# PREPROCESSING
def str_to_int(input_str):
    return [ord(char) for char in input_str]

def str_to_strbin(input_str):
    result = ""
    for char in input_str:
        result += format(ord(char), "08b")
    return "".join(result)

# READ AND WRITE FILE
def read_file(filename):
    path = filename

    with open(path, 'rb') as file:
        temp = []
        byte = file.read(1)
        while byte:
            temp.append(int.from_bytes(byte, "big"))
            byte = file.read(1)

        temp = [bin(bits)[2:] for bits in temp]
        result = []
        for i in temp:
            if len(i) < 8:
                i = (8 - len(i)) * "0" + i
            result.append(i)
        return "".join([chr(int(i,2)) for i in result])

def write_file(filename, content):
    path = filename

    with open(path, 'wb') as file:
        bytes = []
        for char in content:
            byte = int.to_bytes(ord(char), 1, "big")
            bytes.append(byte)
        file.write(b"".join(bytes))

# Modified RC4
key = None
def get_key(key_input):
    global key
    key = key_input

def xor_text(text, keystream):
    result = ""
    text_int = str_to_int(text)
    for i in range(len(text_int)):
        result += chr(text_int[i] ^ keystream[i % len(keystream)])
    return result

def LFSR(input_text, subkey):
    def xor_bits(bits):
        result = 0
        for bit in bits:
            result ^= bit
        return result
    
    register = [1 if bit == "1" else 0 for bit in subkey]
    keystream = []
    i = 0
    while i < len(input_text):
        temp = "0b"
        for _ in range(8):
            register.append(xor_bits(register))
            temp += str(register.pop(0))
        keystream.append(int(temp, 2))
        i += 1
    return keystream

def key_scheduling(key):
    key = str_to_strbin(key)
    temp = [i for i in range(256)]
    key_size = len(key)
    j = 0
    for i in range(256):
        j = (j + temp[i] + int(key[i % key_size])) % 256
        temp[i], temp[j] = temp[j], temp[i]
    
    first_scramble = [i for i in range(key_size)]
    for i in range(256):
        j = ((j + temp[i]) ^ (ord(key[i % key_size]) + first_scramble[i % key_size])) % 256
        temp[i], temp[j] = temp[j], temp[i]
    
    second_scramble = [i for i in range(key_size + 10)]
    for i in range(256):
        j = ((j + temp[i]) ^ (ord(key[i % key_size]) + second_scramble[i % key_size + 10])) % 256
        if (j % 2 == 0 and temp[i] % 2 == 0):
            j = (int((j + temp[i])/2 + 50)) % 256
        else:
            j = (int((j + temp[i])//2 + 25)) % 256
        temp[i], temp[j] = temp[j], temp[i]
    return temp

# ENCRYPT AND DECRYPT
def encrypt(plain):
    global key
    S = key_scheduling(key)
    i = j = 0
    cipher = ""
    for idx in range(len(plain)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        temp = (S[i] + S[j]) % 256
        u = S[t]
        cipher_bytes = u ^ ord(plain[idx])
        cipher += chr(cipher_bytes)
    cipher = xor_text(cipher, LFSR(cipher, S))

    return cipher

def decrypt(cipher):
    global key
    S = key_scheduling(key)
    cipher = xor_text(cipher, LFSR(cipher, S))
    i = j = 0
    plain = ""
    for idx in range(len(cipher)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        temp = (S[i] + S[j]) % 256
        u = S[temp]
        plain_bytes = u ^ ord(cipher[idx])
        plain += chr(plain_bytes)
    
    return plain





