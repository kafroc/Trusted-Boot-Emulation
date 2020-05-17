import sys
from hashlib import sha256
import base64
import hashlib
import os
import json


class cpu():
    def __init__(self):
        self.curpath = os.path.dirname(__file__)
        with open(self.curpath + '/cpu.config') as fp:
            conf = json.load(fp)
        self.sec_boot = conf['sec_boot']

    def run(self):
        print('system starting ...')

        if self.sec_boot == True:
            print('Read RSA Public Key from Flash and Calculate the hash value')
            with open(self.curpath + '/../Flash/uboot/RSA_Pub') as fp:
                pubk = fp.read()
                m = hashlib.sha256()
                m.update(pubk.encode())
                A = base64.b64encode(m.digest()).decode()

            print('Read the hash of RSA Public Key in OTP')
            with open(self.curpath + '/../OTP/RSA_Pub_Hash') as fp:
                B = fp.read()
            if A != B:
                print('RSA Public key is modified.')
                self.down()
                exit(1)
            print('Verify RSA Public Key OK.')

            print('Calculate the sha256 of uboot')
            with open(self.curpath + '/../Flash/uboot/uboot_Version') as fp:
                ver = fp.read()

            with open(self.curpath + '/../Flash/uboot/uboot.py') as fp:
                ub = fp.read()

            uh = int.from_bytes(
                sha256((ver + ub).encode()).digest(), byteorder='big')

            print('verify u-boot signature')
            with open(self.curpath + '/../Flash/uboot/uboot_signature') as fp:
                sig = fp.read()
                hashFromSignature = pow(
                    int(sig, 0), int(pubk.split(':')[0], 0), int(pubk.split(':')[1], 0))
                if hashFromSignature != uh:
                    print('u-boot is modified.')
                    self.down()

            print('uboot verify OK.')

            print('Check u-boot version ... ')
            with open(self.curpath + '/../Flash/uboot/uboot_Version') as fp:
                fv = fp.read()
            with open(self.curpath + '/../OTP/u-boot_Version') as fp:
                ov = fp.read()
            if not self.checkversion(fv, ov):
                print('downgrade version of u-boot.')
                self.down()
        sys.path.append("/../")
        from Flash.uboot.uboot import uboot
        uboot()

    def checkversion(self, fv, ov):
        ovl = ov.split('.')
        fvl = fv.split('.')
        ml = min(len(ovl), len(fvl))
        for i in range(ml):
            try:
                on = int(ovl[i])
                fn = int(fvl[i])
                if on > fn:
                    return False
                if on < fn:
                    return True
            except:
                return False
        if len(ovl) > len(fvl):
            return False
        return True

    def down(self):
        print('system down')
        exit(1)
