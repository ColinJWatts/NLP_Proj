from sequentialTopicModel import TopicModel
import torch

print("Would you like to test on magic, warframe, or current events")
test = ""
channel = None
while test == "":
    test = input()
    if test == "magic":
        channel = "magic-the-shittening"
    elif test == "warframe":
        channel = "space-ninjas-n-shit"
    elif test == "events" or test == "current" or test == "current events":
        channel = "covid-n-shit"
    else:
        test = ""
        print("Could not parse the input, please try again")

numMessages = 12
model = TopicModel(numMessages=numMessages, channel=channel)

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

