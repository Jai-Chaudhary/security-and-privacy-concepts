#! /usr/local/bin/python
# gen.py

import random
import sys
import string
import re

def tokenizer(p):
    """
    Return tokenized substrings of words, numbers and special characters
    """
    strL = ''
    strD = ''
    strS = ''
    for c in p:
        if c in string.ascii_letters:
            strL += c
        elif c in string.digits:
            strD += c
        else:
            strS += c
    return strL, strD, strS

def jumble(strL, strD, strS):
    return random.shuffle([strL, strD, strS]])

def substitute(strL, strD, strS):
    strD = [random.choice(string.ascii_letters) for digit in strD]
    strS = [random.choice(string.punctuation) for punctuation in strS]
    strL = substituteString(strL)
    return [strL, strD, strS]

def truncation(strL, strD, strS):
    strD = strD(:random.randint(len(strD)))
    strS = strS(:random.randint(len(strS)))
    strTot = []
    strTot += if  random.randint(2) == 0 : [] else strD
    strTot += if  random.randint(2) == 0 : [] else strL
    strTot += if  random.randint(2) == 0 : [] else strS
    return strTot

def addition(strL, strD, strS):
    strD.append(random.randrange(3))
    strS.append(string.punctuation[random.randrange(3)])
    strL.append(additionSubstring(strL))

    return [strL, strD, strS]

def randomizeTransformation(strTot):
    [strL, strD, strS]  = tokenizer(strTot)
    transf = random.randint(4)    
    if (transf == 0):
        return ''.join(jumble(strL, strD, strS))
    elif (transf == 1):
        return ''.join(substitute(strL, strD, strS))
    elif (transf == 2):
        return ''.join(truncation(strL, strD, strS))
    elif (transf == 3):
        return ''.join(addition(strL, strD, strS))


def read_password_files(filenames):
    """ 
    Return a list of passwords in all the password file(s), plus 
    a proportional (according to parameter q) number of "noise" passwords.
    """
    pw_list = [ ]
    if len(filenames)>0:
        for filename in filenames:
            if sys.version_info[0] == 3:
                lines = open(filename,"r",errors='ignore').readlines()
            else:
                lines = open(filename,"r").readlines()
            for line in lines:
                pw_list.extend( line.split() )
    else:
        lines = high_probability_passwords.split()
        for line in lines:
            pw_list.extend( line.split() )
    return pw_list


def make_honeyword(pw_list, givenPwd):
    """ 
    make a random password like those in given password list
    """
    # start by choosing a random sugarword from the list
    if len(pw_list) == 0:
        return randomizeTransformation(givenPwd)
    else:
        sugarWords = random.sample(pw_list, random.randint(2, 6))
        sugarWords.append(givenPwd)
        return [randomizeTransformation(sugarword) for sugarword in sugarWords]
    
def generate_passwords( n, pw_list ):
    """ print n passwords and return list of them """
    ans = [ ]
    for t in range( n ):
        pw = make_honeyword(pw_list)
        ans.append( pw )
    return ans

def main():
    # get number of passwords desired
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 19
    # read password files
    filenames = sys.argv[2:]           # skip "gen.py" and n   
    pw_list = read_password_files(filenames)
    # generate passwords
    new_passwords = generate_passwords(n,pw_list)
    # shuffle their order
    random.shuffle(new_passwords)
    # print if desired
    printing_wanted = True
    if printing_wanted:
        for pw in new_passwords:
            print (pw)

# import cProfile
# cProfile.run("main()")

main()


