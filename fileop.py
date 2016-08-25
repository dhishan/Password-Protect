import os
import json
import commands
import sys

PFILE = "upass.data"


def writetofile(jobj):
    path = os.path.dirname(os.path.abspath(__file__))
    changePermission(path)
    path = os.path.join(path,PFILE)
    content = "[]\n"
    conct = ""
    if(os.path.isfile(path)):
        conct = ", "
        try:
            print "Reading upass.data"
            file_obj = open(path,"r")
            content = file_obj.read()
            jc = json.loads(content)
            file_obj.close()
        except ValueError as v:
            content = "[]\n"
            conct = ""
            print v
        except IOError as I:
            print I
            return False
    content = content[:-2] + conct + jobj + "]\n"
    try:
        print "Writing content"
        fp = open(path,"w")
        fp.write(content)
        fp.close()
    except IOError as i:
        print i
        return False
    return True


def readfromfile():
    path = os.path.dirname(os.path.abspath(__file__))
    changePermission(path)
    path = os.path.join(path,PFILE)
    jobj = json.loads("[]")
    if(os.path.isfile(path)):
        try:
            fp = open(path,"r")
            objstring = fp.read()
            jobj = json.loads(objstring)
        except IOError as I:
            # print I
            return jobj
        except ValueError as v:
            # print v
            return jobj
    return jobj


def changePermission(path):
    stat = os.access(path, os.W_OK)
    if(not stat):
        try:
            print "No write permissions at this location"
            print "Attempting chmod 777"
            if(commands.getoutput("echo $(chmod 777 .)") != ""):
                print "Not successful. Change manually"
                return False
            print "permission change success"
            stat = True
        except:
            print "Not successful. Change manually"
            sys.exit(1)
    return stat


def writeMp(mphash):
    path = os.path.dirname(os.path.abspath(__file__))
    changePermission(path)
    path = os.path.join(path,PFILE)
    content = "[]\n"
    if(os.path.isfile(path)):
        try:
            print "Writing Master Password"
            fp = open(path,"w")
            content = content[:-2] + mphash + "]\n"
            fp.write(content)
            fp.close()
        except IOError as I:
            # print I
            return False
    return True

# [{"uname": "dhishan", "ivn": 7475, "mode": 1, "lpass": [43, 171, 206, 43, 92, 193, 252, 104, 100, 30, 227, 20, 11, 29, 238, 57]}]
# jobj1 = json.loads(content)
# print jobj1
# print type(jobj1)
# print jobj1[0]['uname']
