from random import randint


def randomString1(ivn,length):
    rstring = ""
    rnum = ivn
    counter = 1
    while(len(rstring) < length):
        rchar = chr(rnum % 74 + 48)
        rstring += rchar
        rnum += 2
        rnum *= 7
        rnum /= counter
        counter += 1
        if(rnum <= 1):
            rnum = ivn + 2
    return rstring


def randomString2(ivn,length):
    rstring = ""
    rnum = ivn
    counter = 1
    while(len(rstring) < length):
        rchar = chr(rnum % 74 + 48)
        rstring += rchar
        rnum += 5
        rnum *= 3
        rnum /= counter
        counter += 1
        if(rnum <= 1):
            rnum = ivn + 2
    return rstring


def randomnum(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)
