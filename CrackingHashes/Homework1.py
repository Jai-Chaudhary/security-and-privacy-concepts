import hashlib
import csv

hash_file = open('medallionhashes.txt','r')
medallion_file = open('Relevant_Medallion.csv', 'rb')
hash_list = hash_file.readlines()
medallion_list = csv.reader(medallion_file)

for medallion_info in medallion_list:
    for medallion_hash in hash_list:
        if hashlib.sha256(medallion_info[0]).hexdigest() in medallion_hash:
            print medallion_info, medallion_hash