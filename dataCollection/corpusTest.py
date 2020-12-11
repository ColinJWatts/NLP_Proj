from Librarian import Librarian
import numpy as np
import sys
sys.path.append("..\\topicModeling")
import util

punctuation = ['.', ',', '!', '?', '"']

lib = Librarian()
corpus = lib.getCorpus()

print(f"Num Messages: {len(corpus)}")
vocab = []
vocabCount = []
vocabLookup = {}

channels = []
channelCounts = {}
for doc in corpus:
    if not doc["channel"] in channels:
        channels.append(doc["channel"])
        channelCounts[doc["channel"]] = 0

for doc in corpus:
    raw = doc["text"].split()
    for word in raw:
        channelCounts[doc["channel"]] += 1
        w = word.lower()
        for p in punctuation:
            w = w.replace(p, '')
        if not w in vocab:
            vocab.append(w)
            vocabCount.append(1)
            vocabLookup[w] = len(vocab)-1
        else:
            vocabCount[vocabLookup[w]] += 1

newVocab = []
newVocabCount = []
newVocabLookup = {}
for i in range(len(vocab)):
    if vocabCount[vocabLookup[vocab[i]]] > 1:
        newVocab.append(vocab[i])
        newVocabCount.append(vocabCount[i])
        newVocabLookup[vocab[i]] = len(newVocab) - 1
print(f"{len(vocab)}   {len(newVocab)}   {sum(newVocabCount)}   {sum(vocabCount)}")

f = open("vocab.txt", 'w')
for word in newVocab:
    f.write(f"{word.encode('utf8')}\n")
f.flush()
f.close()

noStopWords = util.removeStopwordsFromVocab(vocab)
noStopWordsCount = util.createVocabCount(noStopWords, corpus)
for i in range(20):
    print(f"{noStopWords[np.argmax(noStopWordsCount)]}: {noStopWordsCount[np.argmax(noStopWordsCount)]}")
    noStopWordsCount[np.argmax(noStopWordsCount)] = 0