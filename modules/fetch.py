import discord
from bot import bot, database

async def fetch_channel(channel, timestamp):
    (counts, time) = database.get_channel_counts(channel.id)
    counter = counts + len([msg async for msg in channel.history(limit=None, after=time)])
    database.add_messages_channel(channel.id, timestamp, counter)
    return counter


async def fetch_channel_user(channel, userid, timestamp):
    (counts, time) = database.get_message_counts(userid, channel.id)
    counter = counts + len([msg async for msg in channel.history(limit=None, after=time) if msg.author.id == userid])
    database.add_messages_user(userid, channel.id, timestamp, counter)
    return counter


@bot.command()
async def fetch(ctx):
    """
    Go through every message in the channel and count the messages from the author.
    Then add that to the database.
    """
    counter = await fetch_channel_user(ctx.channel, ctx.message.author.id, ctx.message.created_at)
    await ctx.send(counter)

async def newChannelInfo(channel, timestamp, userid):
    self = ChannelInfo()
    self.channel = channel
    self.channel_count = await fetch_channel(channel, timestamp)
    self.user_count = await fetch_channel_user(channel, userid, timestamp)
    self.username = (await bot.get_user_info(userid)).name
    return self

class ChannelInfo:
    def __init__(self):
        pass

    def __str__(self):
        return f"**{self.channel.name}**: total: {self.channel_count}, total for {self.username}: {self.user_count}"

async def get_top(ctx):
    channels = ctx.message.guild.channels
    timestamp = ctx.message.created_at
    botmember = ctx.message.guild.me

    res = [await newChannelInfo(channel, timestamp, ctx.message.author.id) 
            for (channel) in channels 
            if  isinstance(channel, discord.TextChannel) and 
                channel.permissions_for(botmember).read_message_history]
    return res

@bot.command()
async def top(ctx):
    res = await get_top(ctx)
    await ctx.send([str(chan) for chan in res])
