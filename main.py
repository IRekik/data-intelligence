import nltk
from nltk.corpus import inaugural
from nltk.corpus import stopwords
from nltk.stem.porter import *
import os
import copy

root = os.path.abspath(os.curdir)

list_of_files = [root + '\\reuters21578\\reut2-000.sgm', root + '\\reuters21578\\reut2-001.sgm',
                 root + '\\reuters21578\\reut2-002.sgm']

def parse_document_with_ids(document):
    F = []
    new_id = 0
    trigger = 0
    for i in document:
        if trigger == 1 and i.isnumeric():
            new_id = int(i)
            trigger = 0
        if i == "NEWID=":
            trigger = 1
        else:
            F.append((i, new_id))
    return F

def deduplicate_and_sort(F):
    no_dup_list = set(F)
    no_dup_sorted_list = sorted(no_dup_list, key = lambda x: x[0])
    return no_dup_sorted_list


def aggregate_document_occurrences(no_dup_sorted_list):
    final_list = []
    list_of_indexes = [no_dup_sorted_list[0][1]]
    final_list.append(tuple((no_dup_sorted_list[0], list_of_indexes)))
    list_of_indexes.clear()
    for x in range(1, len(no_dup_sorted_list)):
        list_of_indexes.append(no_dup_sorted_list[x][1])
        if no_dup_sorted_list[x-1][0] != no_dup_sorted_list[x][0]:
            final_list.append(tuple([no_dup_sorted_list[x-1][0], copy.deepcopy(list_of_indexes)]))
            list_of_indexes.clear()
    return final_list


def search_words_in_documents(list_of_words):
    c = 0
    biggest_hit = 0
    most_hits = ""
    for j in list_of_files:
        f = inaugural.raw(list_of_files[c])
        t = nltk.word_tokenize(f)
        p = parse_document_with_ids(t)
        l = deduplicate_and_sort(p)
        a = aggregate_document_occurrences(l)
        for k in a:
            if k[0] in list_of_words:
                print("In document " + str(j) + ', the word ' + str(k[0]) + ' has been found at the DocIDs ' + str(k[1]))
                if len(str(k[1])) > biggest_hit:
                    most_hits = str(j)
                    biggest_hit = len(str(k[1]))
        c = c + 1
    if most_hits != "":
        print(str(k[0]), " has the biggest hit in document ", most_hits)

def test():
    challenge_queries = []
    user_input = input("Please enter a word or quit with q\n")
    while user_input != "q":
        challenge_queries.append(user_input)
        user_input = input("Please enter a word or quit with q\n")
    print(challenge_queries)
    search_words_in_documents(challenge_queries)


print("===================")
print("SUBPROJECT 2")
print("===================")

test()