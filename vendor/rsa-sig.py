from Crypto import Random
from Crypto.PublicKey import RSA
import base64
from hashlib import sha256
import os


with open('uboot-partition/uboot_Version') as fp:
    ver = fp.read()
with open('uboot-partition/uboot.py') as fp:
    uboot = fp.read()

uh = int.from_bytes(sha256((ver + uboot).encode()).digest(), byteorder='big')

'''
keyPair = RSA.generate(bits=2048)
prikey = hex(keyPair.d) + ':' + hex(keyPair.n)
with open('RSA_Pri', 'w') as fp:
    fp.write(prikey)
pubkey = hex(keyPair.e) + ':' + hex(keyPair.n)
with open('RSA_Pub', 'w') as fp:
    fp.write(pubkey)
signature = pow(uh, keyPair.d, keyPair.n)
'''

with open('RSA_Pri') as fp:
    pik = fp.read()
signature = pow(uh, int(pik.split(':')[0], 0), int(pik.split(':')[1], 0))
print("Signature:", hex(signature))

with open('uboot-partition/uboot_signature', 'w') as fp:
    fp.write(hex(signature))
os.system('cp pubkey uboot-partition/RSA_Pub')

with open('RSA_Pub') as fp:
    pk = fp.read()

hashFromSignature = pow(signature, int(
    pk.split(':')[0], 0), int(pk.split(':')[1], 0))
print("Signature valid:", uh == hashFromSignature)
