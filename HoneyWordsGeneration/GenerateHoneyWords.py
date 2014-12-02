#! /usr/local/bin/python

import random
import sys
import string
import argparse

commonDigits = [123, 123456, 12345678, 123456789, 12345, 2580]

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
    strAll = [strL, strD, strS]
    random.shuffle(strAll)
    return strAll

def substitute(strL, strD, strS):
    substitute_strD = []
    substitute_strS = []
    for digit in strD:
        if random.randint(0,100) % 2 == 0:
            substitute_strD += random.choice(string.digits)
        else:
            substitute_strD += digit
    
    for punctuation in strS:
        if random.randint(0,100) % 2 == 0:
            substitute_strS += random.choice(string.punctuation)
        else:
            substitute_strS += punctuation    
    return [strL, strD, strS]

def truncation(strL, strD, strS):
    strD = strD[:random.randint(0,len(strD))]
    strS = strS[:random.randint(0,len(strS))]
    # strTot = []
    # strTot += [] if random.randint(0,100) % 2 == 0 else strD
    # strTot += [] if random.randint(0,100) % 2 == 0 else strL
    # strTot += [] if random.randint(0,100) % 2 == 0 else strS
    return [strL, strD, strS]

def addition(strL, strD, strS):

    strL += str(random.choice(commonDigits)) if random.randint(0,100) % 5 == 0 else ''
    strD += str(random.choice(string.digits)) if random.randint(0,100) % 3 == 0  else ''
    strS += random.choice(string.punctuation) if random.randint(0,100) % 10 == 0  else ''

    return [strL, strD, strS]

def randomizeTransformation(strTot):
    [strL, strD, strS]  = tokenizer(strTot)
    if (random.randint(0,100) % 2 == 0):
        [strL, strD, strS] = jumble(strL, strD, strS)
    if (random.randint(0,100) % 2 == 0):
        [strL, strD, strS] = substitute(strL, strD, strS)
        return ''.join([strL, strD, strS])
    if (random.randint(0,100) % 2 == 0):
        [strL, strD, strS] = truncation(strL, strD, strS)
        return ''.join([strL, strD, strS])
    if (random.randint(0,100) % 2 == 0):
        [strL, strD, strS] = addition(strL, strD, strS)
    return ''.join([strL, strD, strS])


def read_training_password_files(filename):
    """ 
    Return the list of training passwords in given password file
    """
    pw_list = []
    if sys.version_info[0] == 3:
        lines = open(filename,"r",errors='ignore').readlines()
    else:
        print filename
        lines = open(filename,"r").readlines()
    for line in lines:
        pw_list.extend( line.split() )
    return pw_list


def munge_honeyword(original_passwd):
    """ 
    make a random password like those in given password list
    """
    # start by choosing a random sugarword from the list
    if len(pw_list) == 0:
        return randomizeTransformation(original_passwd)
    else:
        sugarWords = random.sample(pw_list, random.randint(2, 6))
        sugarWords.append(givenPwd)
        return [randomizeTransformation(sugarword) for sugarword in sugarWords]

# def munge_honeyword(givenPwd):
#     """ 
#     make a random password like those in given password list
#     """
#     # start by choosing a random sugarword from the list
#     if len(pw_list) == 0:
#         return randomizeTransformation(givenPwd)
#     else:
#         sugarWords = random.sample(pw_list, random.randint(2, 6))
#         sugarWords.append(givenPwd)
#         return [randomizeTransformation(sugarword) for sugarword in sugarWords]
    
# def generate_honeywords_without_training(n, original_passwd):
#     " print n-1 honeywords and original_passwords without training"
#     ans = [ ]
#     for t in range( n ):
#         pw = munge_honeyword(original_passwd)
#         ans.append( pw )
#     return ans

def generate_honeywords_without_training(n, original_passwd):
    " print n-1 honeywords and original_passwords without training"
    honeywords = []
    while len(honeywords) <= n:
        possible_honeyword = randomizeTransformation(original_passwd)
        # print possible_honeyword
        if possible_honeyword not in honeywords:
            if  (len(original_passwd) / 2) < len(possible_honeyword):
                honeywords.append(possible_honeyword)
    return honeywords

def generate_passwords_with_top_100_rock_you(n, original_passwd, sugar_words):
    " print n-1 honeywords and original_passwords without training"
    honeywords = []

    sugar_words_set = random.sample(sugar_words, 2)

    while len(honeywords) <= n/3:
        possible_honeyword = randomizeTransformation(original_passwd)
        # print possible_honeyword
        if possible_honeyword not in honeywords:
            if (len(original_passwd) / 2) < len(possible_honeyword):
                honeywords.append(possible_honeyword) 

    while len(honeywords) <= n:
        print sugar_words_set
        source = random.choice(sugar_words_set)
        possible_honeyword = randomizeTransformation(source)
        # print possible_honeyword
        if possible_honeyword not in honeywords:
            if  (len(original_passwd) / 2) < len(possible_honeyword):
                honeywords.append(possible_honeyword)
    return honeywords


# def generate_passwords_with_full_rock_you(n, original_passwd):
# 

DEFAULT_MODEL = 'train_on_top_100'
MODELS = ['no_training', 'train_on_top_100', 'train_on_all']

def main():
    parser = argparse.ArgumentParser( description = 'HoneyWord Generation' )
    parser.add_argument( 'num' , nargs = '?', type = int, default = 9, help = 'number of honeywords' )
    parser.add_argument( 'passwd_file' , nargs = '?', type = str, default = 'Group5', help = 'original password file' )
    parser.add_argument( 'model' , nargs = '?', type = str, default = DEFAULT_MODEL , choices = MODELS  , help = 'Model type')
    parser.add_argument( 'filename' , nargs = '?', type = str, default = 'rockyou-withcountTop100.txt', help = 'filename to get training passwords from')
    args = parser.parse_args()
    print args

    passwd_file = open(args.passwd_file)
    passwds = passwd_file.read().splitlines()

    for i in range(len(passwds)):
        new_passwords = []

        if i < 100:
            new_passwords += (generate_honeywords_without_training(args.num, passwds[i]))

        elif i < 300:
            pw_list = read_training_password_files(args.filename)
            new_passwords += (generate_passwords_with_top_100_rock_you(args.num, passwds[i], pw_list))

        elif args.model == 'train_on_all':
            pw_list = read_training_password_files(args.filename)
            new_passwords += (generate_passwords_with_full_rock_you(args.num, passwds[i], pw_list))


        random.shuffle(new_passwords)
        # print if desired
        printing_wanted = True
        honey_words_file = open(str(i + 1), 'w+')
        for pw in new_passwords:
            honey_words_file.write(str(pw) + '\n')
            # if printing_wanted:
                # print (pw)
        honey_words_file.close()
    print('HoneyWord File:' + str(i + 1))
        



# import cProfile
# cProfile.run("main()")

if __name__ == '__main__':
    main()
