import util
import sys
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from TopicClassifier import TopicClassifier

sys.path.append("..\\dataCollection")
from Librarian import Librarian

class TopicModel():
    def __init__(self, numMessages=15, channel="space-ninjas-n-shit"):
        self.numMessages = numMessages
        self.lib = Librarian()
        self.channel = channel
        corpus = self.lib.getCorpus()
        corpus = util.removeChannelsFromCorpus(corpus, ["bots-n-shit"])
        corpus = util.cleanPunctuationFromAllDocs(corpus)
        vocab = util.createVocab(corpus)
        vocab = util.removeStopwordsFromVocab(vocab)
        self.vocab = util.removeSingletonsFromVocab(vocab, corpus)
        self.vocabLookup = util.createLookup(self.vocab)

        inChannel = []
        outChannel = []

        for doc in corpus:
            if doc["channel"] == self.channel:
                inChannel.append(util.oneHotEncode(doc, self.vocab))
            else:
                outChannel.append(util.oneHotEncode(doc, self.vocab))

        random.shuffle(inChannel)
        random.shuffle(outChannel)

        tempInTest = inChannel[0:int(len(inChannel)/10)]
        tempInTrain = inChannel[int(len(inChannel)/10):len(inChannel)]

        tempOutTest = outChannel[0:int(len(outChannel)/10)]
        tempOutTrain = outChannel[int(len(outChannel)/10):len(outChannel)]
        
        self.trainingSet = {}
        self.trainingSet["in"] = tempInTrain
        self.trainingSet["out"] = tempOutTrain

        self.testSet = {}
        self.testSet["in"] = tempInTest
        self.testSet["out"] = tempOutTest
        print("Begin training")
        self.train()

    def getSample(self, training=True, isIn=None):
        s = {}
        if training:
            s = self.trainingSet
        else:
            s = self.testSet
        
        label = 0 
        sampleFrom = None  
        if isIn is None:
            temp = random.random()
            if temp > 0.5:
                isIn = True
                sampleFrom = s["in"]
                label = 1
            else:
                isIn = False
                sampleFrom = s["out"]

        samples = random.sample(sampleFrom, self.numMessages)

        return samples, label      


    def train(self, numSteps=1000):
        self.model = TopicClassifier(self.numMessages, self.vocab)
        self.model.train()
        optimizer = optim.Adam(self.model.parameters())
        optimizer.zero_grad()
        criteria = nn.BCELoss()
        batchSize = 10

        for i in range(numSteps):
            target = []
            sampleSet = []
            for j in range(batchSize):
                samples, label = self.getSample(training=True)
                sample = [1] * len(samples[0])
                for s in samples:
                    for k in range(len(sample)):
                        sample[k] += s[k]
                #sample = np.array(sample)
                sampleSet.append(sample)
                target.append(label)
            target = torch.Tensor(target).unsqueeze(1)
            #sampleSet = np.array(sampleSet).unsqueeze(0)
            outputs = self.model(torch.Tensor(sampleSet))


            loss = criteria(outputs, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if i % 100 == 0:
                print(f"Step {i}")
                print(f"Loss: {loss}")
                self.model.eval()
                self.evaluate()
                self.model.train()

        self.model.eval()

    def evaluate(self, numTrials=1000):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        
        for i in range(numTrials):
            samples, label = self.getSample(training=False)
            if label == 1: 
                if self.isOnTopic(samples):
                    tp += 1
                else:
                    fn += 1
            else:
                if self.isOnTopic(samples):
                    fp += 1
                else:
                    tn += 1
        print(f"Accuracy: {(tp + tn)/numTrials}")
        return tp, tn, fp, fn

    def isOnTopic(self, messageSet):
        if len(messageSet) != self.numMessages:
            raise Exception("Incorrect message set size")

        sample = [1] * len(messageSet[0])
        for s in messageSet:
            for i in range(len(sample)):
                sample[i] += s[i]                    
                        

        result = self.model(torch.Tensor(sample))
        if result.item() > 0.7:
            return True
        else:
            return False