# My Own Stream Cipher
from pathlib import Path
import codecs
import base64
import binascii

# untuk proses file dalam byte
def write_byte_file(filename, bytes):
    with open(filename, "wb") as binary_file:
        binary_file.write(bytes)

def open_byte_file(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        return contents

def ksa(key):
    S = list(range(256))
    # nilai j yg digunakan adalah jumlah biner dari key yang dimasukkan
    j = 0
    for ord in key:
        j += ord
    
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(plain, S):
    keystream = []
    i = 0
    j = 0
    for c in range(len(plain)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) % 256
        key = S[t]
        keystream.append(key)
    return keystream

def lfsr(key):
    # ngebuat key nya jadi biner dulu sebelum digeser
    bits = bin(int(binascii.hexlify(key.encode('ISO-8859-1')), 16))
    print(bits)
    # ngilangin 0b depannya
    bit = bits[2:].zfill(8*len(key))
    print(bit[-1])
    new_key = ""
    for i in range(len(bit)):
        xor = str(int(bit[0]) ^ int(bit[-1])) # bit paling blkg di xor sm bit paling depan
        lastBit = bit[-1]
        bit = bit[:-1] # buang bit akhir
        bit = str(xor) + bit # masukin hasil xor nya kedepan
        new_key += lastBit # masukin keluaran nya ke key baru
    base10 = int(new_key, 2) #ubah lagi ke strs
    hexStr = '%x' % base10
    length = len(hexStr)
    byte = binascii.unhexlify(hexStr.zfill(length + (length & 1)))
    return codecs.decode(byte, 'ISO-8859-1')

''' 
untuk enkrip dekrip dimodifikasi bagian XOR nya menjadi 
melakukan prosedur extended vigenenere cipher
'''
def enkrip(plain, key):
    plain = list(plain)
    # key nya di lfsr dulu
    key = lfsr(key)
    # ubah key jadi dapat bentuk biner
    key = [ord(c) for c in key]
    # bikin key stream
    keystream = prga(plain, ksa(key))

    hasil = []
    for i in range(len(plain)):
        val = ("%02X" % ((ord(plain[i]) + keystream[i])%256)) # hasil nya dibikin hex
        hasil.append(val)
    return ''.join(hasil)

def dekrip(cipher, key):
    cipher = codecs.decode(cipher, 'hex_codec')
    cipher = list(cipher)
    # key nya di lfsr dulu
    key = lfsr(key)
    # ubah key jadi dapat bentuk biner
    key = [ord(c) for c in key]
    # bikin key stream
    keystream = prga(cipher, ksa(key))

    hasil = []
    for i in range(len(cipher)):
        val = ("%02X" % ((cipher[i] - keystream[i] + 256)%256)) # hasil nya dibikin hex
        hasil.append(val)
    text = ''.join(hasil)
    return codecs.decode(text, 'hex_codec').decode('ISO-8859-1')

# fungsi enkrip dekrip untuk input-an file
def enkripFile(path, key):
    file = open_byte_file(path)
    file = file.decode("ISO-8859-1")
    en = enkrip(file, key)
    en = en.encode("ISO-8859-1")
    return en

def dekripFile(path, key):
    file = open_byte_file(path)
    file = file.decode("ISO-8859-1")
    de = dekrip(file, key)
    de = de.encode("ISO-8859-1")
    return de

# fungsi untuk convert
def hex_to_base64(bin):
    return codecs.encode(codecs.decode(bin, 'hex'), 'base64').decode()

def base64_to_hex(b):
    h = base64.b64decode(b).hex()
    return h

def str_to_base64(string):
    bstring = string.encode('ascii')
    base64_byte = base64.b64encode(bstring)
    base64_message = base64_byte.decode('ascii')
    return base64_message

def str_to_hex(string):
    hexx = []
    for c in string:
        h = "%02X" % (ord(c))
        hexx.append(h)
    return (''.join(hexx))

