# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
client = discord.Client(intents=intents)

todoList = {}


@client.event
async def on_ready():
    for guild in client.guilds:
        # print(f'{guild.name} (id: {guild.id})')
        if guild.name == GUILD:
            break

    print(
        f'{client.user} has connected to Discord!'
        f'{guild.name} (id: {guild.id})'
    )

    # Getting all server members
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

# DMs members that join the server
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

# Checks messages sent in the server
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

    print(f'New message -> {message.author} said: {message.content}')
    
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday!')
        await message.channel.send(message.content)

    # Help
    if '!todo help' in message.content.lower():
        await message.channel.send(
            'Available Commands: ' + 
            '\n !todo create (name) ' +
            '\n\t-Creates a To Do List. ' +
            '\n !todo add (name) (item) ' +
            '\n\t-Adds item to a specific To Do List ' +
            '\n !todo check (name) ' +
            '\n\t-Checks a specific To Do List ' +
            '\n!todo delete (name) (number) ' +
            '\n\t-Deletes a specific item in the To Do List ' +
            '\n!todo remove (name) ' +
            '\n\t-Removes a specific list ' +
            '\n!todo all ' +
            '\n\t-Checks all the Todo List'
                                   )
    # Creates a List
    elif '!todo create' in message.content.lower():
        message_array = message.content.lower().split(' ')
        todoList[message_array[2]] = []
        await message.channel.send(message_array[2] + ' todo list has been created.')
    # Adds to a specific List
    elif '!todo add' in message.content.lower():
        message_array = message.content.lower().split(' ')
        temp = ""
        for x in range(3, len(message_array)):
            temp += message_array[x] + " "
        if message_array[2] in todoList:
            todoList[message_array[2]].append(temp)
            await message.channel.send(todoList[message_array[2]])
        else:
            await message.channel.send('List does not exist.')
    # Checks a specific List
    elif '!todo check' in message.content.lower():
        message_array = message.content.lower().split(' ')
        index = 1
        if message_array[2] in todoList:
            await message.channel.send(message_array[2] + " To-Do List:\n")
            for x in range(len(todoList[message_array[2]])):
                await message.channel.send(f'{index}) {todoList[message_array[2]][x]}')
                index += 1
        else:
            await message.channel.send('List does not exist.')
    # Deletes a specific item in the specific List
    elif '!todo delete' in message.content.lower():
        message_array = message.content.lower().split(' ')
        try:
            temp = todoList[message_array[2]].pop(int(message_array[3])-1)
            await message.channel.send('Deleting the item ' + temp)
        except ValueError:
            await message.channel.send('Item in the To Do List does not exist.')
        except IndexError:
            await message.channel.send('Item in the To Do List does not exist.')
    # Removes the entire list in the To Do List
    elif '!todo remove' in message.content.lower():
        message_array = message.content.lower().split(' ')
        try:
            todoList.pop(message_array[2],None)
            await message.channel.send('Deleting the To Do List ' + message_array[2] + '.')
        except KeyError:
            await message.channel.send('List does not exist.')
    # Checks all To Do Lists
    elif '!todo all' in message.content.lower():
        await message.channel.send(todoList)

client.run(TOKEN)