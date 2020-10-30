
def createLookup(vocab):
    lookup = {}
    for i in range(len(vocab)):
        lookup[vocab[i]] = i
    return lookup

def oneHotEncode(doc, vocab, addOneReg=False):
    text = doc["text"].split()
    x = 0
    if addOneReg:
        x = 1
    result = [x] * len(vocab)
    lookup = createLookup(vocab)
    for word in text:
        if word in vocab:
            result[lookup[word]] += 1
    return result

def createVocab(corpus):
    vocab = []
    for doc in corpus:
        text = doc["text"].split()
        for word in text:
            w = word.lower()
            if not w in vocab:
                vocab.append(w)

    return vocab

def removeChannelsFromCorpus(corpus, channels):
    newCorpus = []
    for doc in corpus:
        if not doc["channel"] in channels:
            newCorpus.append(doc)
    return newCorpus

def removeStopwordsFromVocab(vocab, stopwordFile="./stopwords.txt"):
    newVocab = []
    f = open(stopwordFile, 'r')
    stopwords = f.read().splitlines()
    for word in vocab:
        if not word in stopwords:
            newVocab.append(word)
    return newVocab

def removeSingletonsFromVocab(vocab, corpus):
    lookup = createLookup(vocab)
    count = [0] * len(vocab)

    for doc in corpus:
        text = doc["text"].split()
        for word in text:
            w = word.lower()
            if w in vocab:
                count[lookup[w]] += 1

    result = []
    for i in range(len(vocab)):
        if count[i] > 1:
            result.append(vocab[i])
    return result

def cleanPunctuationFromAllDocs(corpus, punctuaction=['.', ',', '!', '?', '"']):
    newCorpus = []
    for doc in corpus:
        newCorpus.append(cleanPunctuationFromDoc(doc, punctuaction=punctuaction))
    return newCorpus

def cleanPunctuationFromDoc(doc, punctuaction=['.', ',', '!', '?', '"']):
    text = doc["text"]

    for p in punctuaction:
        text = text.replace(p, '')

    doc["text"] = text
    return doc