import discord
import util
from sequentialTopicModel import TopicModel
import torch

targetChannel = "magic-the-shittening"
numMessages = 12
model = TopicModel(numMessages=numMessages, channel=targetChannel)
client = discord.Client()

zeroVec = [0] * len(model.vocab)
val = model.model(torch.Tensor(zeroVec))
print(val)

messageStorage = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    id = str(message.author.id)
    if message.author == client.user:
        return
    if len(message.content) > 0:
        if message.channel in messageStorage.keys():
            if len(messageStorage[message.channel]) >= numMessages:
                messageStorage[message.channel] = messageStorage[message.channel][1:len(messageStorage[message.channel])]
                messageStorage[message.channel].append(model.lib.createDoc(id, message.channel, message.content))

                messageSet = []
                for m in messageStorage[message.channel]:
                    messageSet.append(util.oneHotEncode(m, model.vocab))

                if str(message.channel) != targetChannel and model.isOnTopic(messageSet,True):
                    await message.channel.send(f"HEY! This channel is not for that topic! Get back to {targetChannel}!!!")
                    messageStorage[message.channel] = []
            else: 
                messageStorage[message.channel].append(model.lib.createDoc(id, message.channel, message.content))

        elif str(message.channel) != targetChannel:
            messageStorage[message.channel] = [model.lib.createDoc(id, message.channel, message.content)]


f = open("./token.txt", 'r')
token = f.read()
client.run(token)