from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import SHA256
import fileop as fp
import uuid
import randgen as rg
import json


class Encrypter(object):
    def __init__(self,creds):
        self.udata = creds

    def __generatekey(self):
        return rg.randomString1(self.udata.ivn,AES.block_size - len(self.udata.uname)) + self.udata.uname

    def __generateiv(self):
        return rg.randomString1(self.udata.ivn,AES.block_size)

    def __passwordlenght(self):
        return self.udata.password + rg.randomString2(self.udata.ivn,AES.block_size - len(self.udata.password))

    def __generatectr(self):
        return Counter.new(128)

    def encryptpass(self):
        epass = ""
        # key 16 characters
        key = self.__generatekey()
        # IV for
        if self.udata.mode not in (1,6):  # IV needed only for CBC
            iv = self.__generateiv()
            ciper = AES.new(key,self.udata.mode,iv)
        elif self.udata.mode is 6:
            ctr = self.__generatectr()
            ciper = AES.new(key,self.udata.mode,counter=ctr)
        else:
            ciper = AES.new(key,self.udata.mode)
        epass = ciper.encrypt(self.__passwordlenght())
        return epass

    def decryptpass(self):
        paswd = ""
        key = self.__generatekey()
        if self.udata.mode not in (1,6):  # IV needed only for CBC
            iv = self.__generateiv()
            ciper = AES.new(key,self.udata.mode,iv)
        elif self.udata.mode is 6:
            ctr = self.__generatectr()
            ciper = AES.new(key,self.udata.mode,counter=ctr)
        else:
            ciper = AES.new(key,self.udata.mode)
        paswd = ciper.decrypt(''.join(chr(i) for i in self.udata.lpass))
        return paswd[:self.udata.plen]


class MasterPass(object):
    def __init__(self):
        pass

    def isexist(self):
        jobj = fp.readfromfile()
        for elem in jobj:
            if(elem.get('msp')):
                return True
        return False

    def isvalid(self,pwd):
        phash = self.__generatehash(pwd)
        # print phash
        jobj = fp.readfromfile()
        for elem in jobj:
            if(elem.get('msp')):
                if(elem.get('msp') == phash):
                    return True
        return False

    def __generatehash(self,pwd):
        uniqID = uuid.getnode()
        # print uniqID
        paswd = pwd + "-" + str(uniqID)
        # print paswd
        h = SHA256.new(paswd)
        return h.hexdigest()

    def storepass(self,pwd):
        hashval = self.__generatehash(pwd)
        # print hashval
        pobj = {'msp':hashval}
        json_obg = json.dumps(pobj)
        return fp.writeMp(json_obg)

# [{"uname": "dhishan", "ivn": 5806, "plen": 10, "mode": 1, "lpass": [89, 246, 178, 39, 40, 223, 166, 91, 247, 162, 136, 16, 195, 39, 160, 134]}, {"uname": "dhishan", "ivn": 5183, "plen": 11, "mode": 6, "lpass": [195, 117, 249, 119, 144, 117, 234, 105, 38, 188, 106, 22, 90, 62, 100, 113]}, {"uname": "chinku311", "ivn": 8478, "plen": 7, "mode": 2, "lpass": [242, 178, 16, 189, 203, 211, 47, 185, 73, 116, 76, 118, 107, 176, 75, 58]}, {"uname": "prp", "ivn": 8217, "plen": 12, "mode": 6, "lpass": [215, 176, 213, 255, 194, 65, 78, 60, 248, 104, 4, 195, 107, 123, 38, 150]}]
