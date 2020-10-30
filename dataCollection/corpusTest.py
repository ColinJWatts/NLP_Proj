from Librarian import Librarian

punctuation = ['.', ',', '!', '?', '"']
# punctuation = []

lib = Librarian()
corpus = lib.getCorpus()

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
print(len(newVocab))
# print(newVocab)
# print(f"{len(newVocab)}   {sum(newVocabCount)}   {sum(vocabCount)}")

for word in vocab:
    if 'deque' in word:
        print(f"{word}: {newVocabCount[newVocabLookup[word]]}")



# print(channelCounts)