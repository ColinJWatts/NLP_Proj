import discord
import time

client = discord.Client()
token = open("./mytoken.txt",'r').read()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    id = str(message.author.id)
    if message.content.startswith('!'):
        try:
            val = int(message.content[1:])
            for i in range(val):
                await message.channel.send(f"{i+1}/{val}")
                time.sleep(0.25)
        except:
            await message.channel.send("Make sure it's an integer after the !")


client.run(token, bot=False)