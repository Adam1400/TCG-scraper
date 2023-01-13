import discord
import responses
import os
from dotenv import load_dotenv
load_dotenv()



async def send_message(message, user_message, is_private):
    try:
        #await message.author.send('Thinking...') if is_private else await message.channel.send('Thinking...')

        response = responses.handel_responses(user_message)
        
        partitioned_response = partition_string(response, 2000)
        for partition in partitioned_response:
            await message.author.send(partition) if is_private else await message.channel.send(partition)


    except Exception as e:
        #await message.author.send('Try again, something is up with that message^') if is_private else await message.channel.send('Try again, something is up with that message^')
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('Token')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(client.user,'is running')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(username,'said:',user_message, channel)

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
         await send_message(message, user_message, is_private=False)



    client.run(TOKEN)

def partition_string(string, length):
    return [string[i:i+length] for i in range(0, len(string), length)]


