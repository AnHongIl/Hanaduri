import tensorflow as tf
import numpy as np
from model import NeuralNetwork
import csv
from collections import Counter
from konlpy.tag import Mecab
import socket
import pickle
import pdb

numbers = []
categories = []
titles = []
contents = []
with open('input_11829.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            numbers.append(row[0])
            categories.append(row[1])
            titles.append(row[2])
            contents.append(row[3])
            
mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic/')
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

word2index = {}
for i, word in enumerate(words):
    word2index[word] = i

targets = set(categories)
targets2index = {}

for i, target in enumerate(targets):
    targets2index[target] = i

#input_size = 29861
#output_size = 11
#print("input size: {}, output size: {}".format(len(word2index), len(targets2index)))

#tf.reset_default_graph()
NN = NeuralNetwork(len(word2index), len(targets2index), 0.001)

save_file = '/mnt/train_1000.ckpt'
saver = tf.train.Saver()

#body = [ "정치", "일상", "교육감", "재선발", "요청", "서울"]

with tf.Session() as sess:
    saver.restore(sess, save_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8002))
    s.listen(0)
    print("Recommendation ready")
    while True:
        client_socket, addr = s.accept()

        dic = client_socket.recv(5000)
        dic = pickle.loads(dic)
        #print("In recommendations received from django title: {}".format(dic['title']))
        #print("In recommendations received from django body: {}".format(dic['body']))
        keywords_title = mecab.nouns(dic['title'])
        keywords_body = mecab.nouns(dic['body'])
        
        print("In recommendations received from django keywords_title: {}".format(keywords_title))
        print("In recommendations received from django keywords_body: {}".format(keywords_body))
        inputs = np.zeros(len(word2index))
        for word in keywords_title:
            if word in word2index:
                inputs[word2index[word]] = 1.0
            else:
                print("{} not exsits in dic".format(word))
                
        for word in keywords_body:
            if word in word2index:
                inputs[word2index[word]] = 1.0
            else:
                print("{} not exsits in dic".format(word))

        output = sess.run(NN.output, feed_dict={NN.inputs: inputs.reshape(-1, len(word2index))})
        index = np.argmax(output)
        for key, value in targets2index.items():
            if value == index:
                results = key
                break
        print("Results: {}".format(results))
        client_socket.send(pickle.dumps(results))
        client_socket.close()
        
