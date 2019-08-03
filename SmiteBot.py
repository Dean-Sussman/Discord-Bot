import discord
import time
import random
from discord.ext import commands

bot = commands.Bot(".")
general_channel_id = 000000000000
alive_role_id = 000000000000
mafia_channel_id = 00000000000000
guild_id = 0000000000000

TOKEN = 'XXXXXXXXXXXXXXXXXXXXX'


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('~hello'):
        channel = message.channel
        await channel.send('Hello!')
    elif message.content.startswith('~roulette'):
        channel = message.channel
        random_user = await random_human(channel)
        await channel.send('{} has been chosen'.format(random_user.mention))
    elif message.content.startswith('~mafia5'):
        channel = message.channel
        if await channel_check(1):
            await mafia(1)
        else:
            await channel.send('5 players must be in the "Mafia" voice channel for the game to begin.'
                               'Re-send the command once all players have joined.')
    elif message.content.startswith('~mafia6'):
        channel = message.channel
        if await channel_check(6):
            await mafia(6)
        else:
            await channel.send('6 players must be in the "Mafia" voice channel for the game to begin.'
                               'Re-send the command once all players have joined.')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(general_channel_id)
    new_member = member.mention
    await channel.send(f'Welcome back to the goon squad, {new_member}')


@bot.event
async def on_member_remove(member):
    member_name = member.display_name
    channel = bot.get_channel(general_channel_id)
    await channel.send(f'Have fun in Florida, **{member_name}**. Come back to us soon')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')


@bot.event
async def mafia(number_of_players):
    channel = bot.get_channel(general_channel_id)
    voice_channel = bot.get_channel(mafia_channel_id)
    mafia_user = await random_human(voice_channel)
    guild = bot.get_guild(guild_id)
    await mafia_user.create_dm()
    await mafia_user.dm_channel.send("You are the mafia!")
    await channel.send(f'Welcome to Discord Mafia! You have chosen to play with {number_of_players} players.'
                       f'In Discord Mafia, there are {number_of_players - 1} town and 1 mafia.'
                       f'The mafia wins when the town no longer makes up a majority of living players.'
                       f'The town wins when the mafia dies.'
                       f'The mafia player has been randomly chosen; check your DMs!'
                       f'If you did not receive a DM, you are town.')
    await channel.send(f'The game is played by cycling between daytime and nighttime. At night, you will be muted.'
                       f'During the night, the player designated as Mafia has 30 seconds to choose who to kill.'
                       f'In order to choose who to kill, the mafia will DM me, SmiteBot, with *********'
                       f'If the mafia does not choose someone in that time frame, I Smite them, and town wins by default')
    await channel.send(f'After fifteen seconds have passed, everyone will wake up and be un-muted, and daytime begins.'
                       f'I will mute and @mention any players who have been killed in the mafia text channel.')
    await channel.send(f'During the day, you have [X] minutes to have a discussion. '
                       f'Discuss any players you think are suspicious.'
                       f'Town players: remember your goal is to find out who the mafia is, and vote them off.'
                       f'Mafia: remember that your goal is to keep suspicions off of you.')
    await channel.send(f'After time is up, you must cast your votes.'
                       f'If you wish to cast your vote early or change your vote, you may.'
                       f'Daytime ends when everyone has voted, irrespective of the time remaining.'
                       f'After time runs out, you **must** vote. Everyone will be muted until votes are cast.')
    alive_role = guild.get_role(alive_role_id)
    await add_role_to_channel(alive_role, voice_channel)
    await channel.send(f'The first night time begins in 60 seconds.'
                       f'The mafia player has been sent a DM with instructions on choosing a target.'
                       f'Good luck!')
    await time.sleep(60)



@bot.event
async def channel_check(number_of_players):
    channel = bot.get_channel(mafia_channel_id)
    if len(channel.members) != number_of_players:
        return False
    else:
        return True


@bot.event
async def random_human(channel):
    random_user = random.choice(channel.members)
    while random_user.bot:
        random_user = random.choice(channel.members)
    return random_user


@bot.event
async def add_role_to_channel(role_id, channel_id):
    member_list = channel_id.members
    for member in member_list:
        await member.add_roles(role_id)

bot.run(TOKEN)
