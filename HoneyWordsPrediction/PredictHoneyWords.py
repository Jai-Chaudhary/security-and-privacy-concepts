#! /usr/local/bin/python

import random
import sys
import string
import argparse
from collections import Counter
import os
import numpy as np
from operator import itemgetter
import distance_metric as distance
import sklearn.cluster as cluster

def repeat_words_strategy(honey_words):
    most_common,num_most_common = Counter(honey_words).most_common(1)[0] # 4, 6 times
    return most_common if num_most_common > 1 else None

def general_user_strategy(honey_words):
    prob_honey_word = {}
    for honey_word in honey_words:
        prob = None
        if honey_word.islower():
            prob = 0.42
        elif honey_word.isupper():
            prob = 0.02
        elif any(j in string.punctuation for j in honey_word):
            prob = 0.03
        elif all(j in string.digits for j in honey_word):
            prob =  0.16
        else:
            prob = 0.4
        prob_honey_word[honey_word] = prob
    return prob_honey_word

def common_char_strategy(honey_words):
    position_char = np.array([[character for character in honey_word] for honey_word in honey_words])
    position_common_char = [Counter(position).most_common(1)[0][0] for position in position_char.T]
    matches = [(honey_word, sum([1 for char, common_char in zip(honey_word, position_common_char) if char == common_char ])) for honey_word in honey_words]
    return max(matches, key=itemgetter(1))[0]

def clustering_strategy(honey_words):
    word_distances = np.array([[distance.levenshtein(honeyword1, honeyword2) for honeyword1 in honey_words] for honeyword2 in honey_words])
    max_distance = np.amax(word_distances)
    max_array = max_distance * np.ones(np.shape(word_distances))
    word_similarities = np.subtract(max_array, word_distances)
    ac = cluster.AgglomerativeClustering(n_clusters =2,linkage="average", affinity="precomputed").fit(np.array(word_similarities))
    sugar_words = []
    if np.count_nonzero(ac.labels_) < (len(honey_words) / 2):
        for index in np.nonzero(ac.labels_)[0]:
            sugar_words.append(honey_words[index])
    else:
         for index in range(len(honey_words) - 1):
            if index not in np.nonzero(ac.labels_)[0]:
                sugar_words.append(honey_words[index])       
    return sugar_words

def attack_all_files(foldername):
    passwords = []
    write_file = open(os.path.join(os.getcwd(), foldername + '_pred_passwords'),'w+')

    for filename in os.listdir(os.path.join(os.getcwd(),foldername)):
        if string.find(filename, 'password') == -1:
            read_file = open(os.path.join(os.path.join(os.getcwd(),foldername), filename),'r')
            honey_words = read_file.read().splitlines()
            read_file.close() 
            if repeat_words_strategy(honey_words) != None:
                passwords.append(repeat_words_strategy(honey_words))
                print repeat_words_strategy(honey_words)
            else:
                cluster_words = clustering_strategy(honey_words)
                if len(cluster_words) == 1:
                    passwords.append(cluster_words[0])
                else:
                    # hybrid strategy
                    common_word = common_char_strategy(honey_words)
                    # find the cluster word closest to the word found by common char strategy
                    closest_cluster_word = cluster_words[np.argmin(np.array([distance.levenshtein(common_word, cluster_word) for cluster_word in cluster_words]))]
                    # return word found by common char strategy or cluster strategy based on general user prob.
                    prob_honey_word = general_user_strategy(honey_words)
                    if prob_honey_word[closest_cluster_word] > prob_honey_word[common_word]:
                        passwords.append(closest_cluster_word)
                    else:
                        passwords.append(common_word)
            write_file.write(str(passwords[-1]) + '\n')
    write_file.close()

    print 'Written the passwords to <honeyword filename>_password' 
    print passwords

def main():
    parser = argparse.ArgumentParser( description = 'HoneyWord Prediciton' )
    parser.add_argument( 'foldername' , nargs = '+', type = str, help = 'foldername to get training passwords from')
    args = parser.parse_args()
    print args

    attack_all_files(args.foldername[0])

if __name__ == '__main__':
    main()
