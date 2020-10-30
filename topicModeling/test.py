from sequentialTopicModel import TopicModel
import torch

numMessages = 12
model = TopicModel(numMessages=numMessages, channel="magic-the-shittening")

n = 10

bestWords = []

worstWords = []

for word in model.vocab:
    wordVector = [0] * len(model.vocab)
    wordVector[model.vocabLookup[word]] = 1
    val = model.model(torch.Tensor(wordVector))
    val = val.item()
    
    if len(bestWords) < n:
        bestWords.append((val, word))
        worstWords.append((val, word))

        bestWords.sort()
        worstWords.sort()
    else:
        if val > bestWords[0][0]:
            bestWords = bestWords[1:len(bestWords)]
            bestWords.append((val, word))
            bestWords.sort()
        if val < worstWords[n-1][0]:
            worstWords = worstWords[0:len(worstWords)-1]
            worstWords.append((val, word))
            worstWords.sort()

bestWords.reverse()
print("Best words:")
print(bestWords)
print("Wrost words: ")
print(worstWords)

