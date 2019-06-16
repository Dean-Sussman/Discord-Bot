import discord
import random
from discord.ext import commands

bot = commands.Bot(".")

TOKEN = 'TOKEN'


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('~hello'):
        channel = message.channel
        await channel.send('Hello!')
    elif message.content.startswith('~roulette'):
        channel = message.channel
        randomuser = random.choice(message.guild.members).mention
        await channel.send('{} has been chosen'.format(randomuser))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL)
    newmember = member.mention
    await channel.send(f'Welcome back to the goon squad, {newmember}')

@bot.event
async def on_member_remove(member):
    membername = member.display_name
    channel = bot.get_channel(CHANNEL)
    await channel.send(f'Have fun in Florida, **{membername}**. Come back to us soon')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')


bot.run(TOKEN)
