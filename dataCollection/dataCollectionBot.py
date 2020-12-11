import discord
import re
from Librarian import Librarian

client = discord.Client()
lib = Librarian(maxDocuments=100)
f = open("./in.txt", 'r')
optedIn = f.read().splitlines()
f.close()
f = open("./token.txt", 'r')
token = f.read()

def updateOptInFile(newList):
    f = open("./in.txt", 'w')
    for i in newList:
        f.write(f"{i}\n")
    f.flush()
    f.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    id = str(message.author.id)
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        if 'help' in message.content.lower():
            await message.channel.send(f"Hello! You have requested help from the data collection bot!\nBy default, none of your data will be tracked and even if you do opt in all user information is obfuscated for storage.\nFurthermore, none of the data collected by this bot will be used for anything other than training bots for academic or entertainment purposes\nAvailable commands:\n$help\n$status\n$opt in\n$opt out")
        elif 'status' in message.content.lower():
            if id in optedIn:
                await message.channel.send(f"Hello {message.author.display_name}! Your data is currently being tracked!")
            else: 
                await message.channel.send(f"Hello {message.author.display_name}! You have not opted in to data collection.")
        elif 'opt' in message.content.lower():
            if 'out' in message.content.lower():
                if id in optedIn:
                    optedIn.remove(id)
                    updateOptInFile(optedIn)
                    await message.channel.send(f"Hello {message.author.display_name}! Your data will no longer be collected for science!")
                else: 
                    await message.channel.send("Parinoia pays off sometimes")
            elif 'in' in message.content.lower():
                if not id in optedIn:
                    optedIn.append(id)
                    updateOptInFile(optedIn)
                await message.channel.send(f"Thank you {message.author.display_name} for your contribution")
        elif 'flush' in message.content.lower():
            lib.saveDocs()
    else:
        if id in optedIn and len(message.content) > 0 and re.search("<@[!&]([0-9])+>", message.content) is None:
            lib.addDocument(id, message.channel, message.content)


client.run(token)