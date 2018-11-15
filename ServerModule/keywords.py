from konlpy.tag import Mecab
import csv
from collections import Counter
import numpy as np

"""
    row[0] : no
    row[1] : category
    row[2] : title
    row[3] : body
"""

numbers = []
categories = []
titles = []
contents = []

with open('input_11829.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #numbers.append(row[0])
        #categories.append(row[1])
        titles.append(row[2])
        contents.append(row[3])

#mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')

for i, title in enumerate(titles):
    titles[i] = mecab.nouns(title)

for i, content in enumerate(contents):
    contents[i] = mecab.nouns(content)

words_counts = Counter()

for title in titles:
    for word in title:
        words_counts[word] += 1

for content in contents:
    for word in content:
        words_counts[word] += 1

words = set(words_counts.keys())
words_size = len(words)
#print(words_size)

word2index = {}

for i, word in enumerate(words):
    word2index[word] = i

import socket
import pickle

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8001))
    s.listen(0)
    print("Keyword ready")
    while True:
        client_socket, addr = s.accept()
        title = client_socket.recv(2000).decode("UTF-8")
        print("redv title : ", title)
        keywords = mecab.nouns(title)
        print("keywords : ", keywords)
        client_socket.send(pickle.dumps(keywords))
        client_socket.close()
except:
    print("Error")


#word2index
"""
targets = set(categories)
targets2index = {}

for i, target in enumerate(targets):
    targets2index[target] = i
targets2index
"""
