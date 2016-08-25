import sys
import json
import commands
import encrypter as ep
import randgen as rg
import fileop as fp
# import string
try:
    username = commands.getoutput("echo $(whoami)")
except:
    print "Commands error"


def uinput(statement):
    print_statement = statement + ": "
    utext = raw_input(print_statement).lower()
    return utext


class credentials():
    def __init__(self):
        self.uname = ""
        self.password = ""
        self.mode = 0
        self.ivn = 0
        self.lpass = []
        self.plen = 0


def newentry():
    user = credentials()
    user.uname = uinput("Enter the user name")
    user.password = raw_input("Enter the password to save: ")
    user.plen = len(user.password)
    user.ivn = rg.randomnum(4)
    print "How do you want to encrypt the password?"
    print "ECB[1]","CBC[2]","CTR[6]"
    choice = uinput("Enter your choice")
    while choice not in ('1','2','6'):
        printErr()
        choice = uinput("Enter your choice")
    user.mode = int(choice)
    eobj = ep.Encrypter(user)
    epass = eobj.encryptpass()
    for c in epass:
        user.lpass.append(ord(c))
    # print eobj.decryptpass()
    python_obj = {"uname":user.uname,"mode": user.mode,"ivn":user.ivn,"lpass": user.lpass,"plen": user.plen}
    json_obg = json.dumps(python_obj)
    return fp.writetofile(json_obg)


def getpassforuser(uname):
    jobj = fp.readfromfile()
    ulist = []
    if(len(jobj) > 0):
        for elem in jobj:
            if(elem.get('uname') == uname):
                user = credentials()
                user.uname = elem.get('uname')
                if(elem.get('ivn')):
                    user.ivn = elem.get('ivn')
                if(elem.get('mode')):
                    user.mode = elem.get('mode')
                if(elem.get('lpass')):
                    user.lpass = elem.get('lpass')
                if(elem.get('plen')):
                    user.plen = elem.get('plen')
                ulist.append(user)
    return ulist


def getpasswrd():
    uname = uinput("Enter the user name")
    ucred = getpassforuser(uname)
    passwrds = []
    if(len(ucred) == 0):
        print "Username not in database"
        return passwrds
    for userd in ucred:
        eobj = ep.Encrypter(userd)
        epass = eobj.decryptpass()
        passwrds.append(epass)
    return passwrds


def checkpasswrd():
    pwds = getpasswrd()
    pswd = raw_input("Enter Password: ")
    for pwd in pwds:
        if(pswd == pwd):
            print "Password Correct"
            return True
    return False


def printErr():
    print "Incorrect Option. RE-Enter your choice"


def main():
    if username:
        print "Hello", username
    print "Welcome to Password Protect..  ",
    print "We protect what matters the most !!!!"
    print "What do you want to do today?"
    valid = False
    mp = ep.MasterPass()
    while(not valid):
        if(not mp.isexist()):
            print "Master Password doesn't Exist. Create new"
            pwd = raw_input("Enter Master Password: ")
            valid = mp.storepass(pwd)
            if not valid:
                print "Write Error!"
                sys.exit(1)
        else:
            pwd = raw_input("Enter Master Password: ")
            valid = mp.isvalid(pwd)
            if not valid:
                print "Invalid Password"

    while(1):
        print
        print "Store a password[S]","Retrieve a password[R]"," Check your password[C]", "Quit[Q]"
        choice = uinput("Enter your choice")
        while choice not in ('s','r','c','q'):
            printErr()
            choice = uinput("Enter your choice")
        if(choice == "s"):
            if(newentry()):
                print "Password Saved Successfuly"
        if(choice == "r"):
            plist = getpasswrd()
            if(len(plist)):
                for pwds in plist:
                    print pwds
        if(choice == "c"):
            if(not checkpasswrd()):
                print "Sorry Incorrect Password"
        if(choice == 'q'):
            sys.exit(1)


if __name__ == "__main__":
    main()
