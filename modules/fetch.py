import discord
from bot import bot, database

import modules.helpers as h

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
    async with ctx.channel.typing():
        counter_user = await fetch_channel_user(ctx.channel, ctx.message.author.id, ctx.message.created_at)
        counter_channel = await fetch_channel(ctx.channel, ctx.message.created_at)
        await h.respond(ctx, description=f"You have **{counter_user}** messages in this channel, making up **{round(counter_user * 100.0 / counter_channel, 2)}%** of the messages!")

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

    def tuple(self):
        return (self.channel.name, self.channel_count, self.username, self.user_count)

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
    (channel_name, channel_count, username, user_count) = zip(*[chan.tuple() for chan in res])
    await h.respond(ctx, fields=[
        ("Channel", "\n".join([f"**{name}**" for name in channel_name]), True),
        ("Counts", "\n".join([str(count) for count in channel_count]), True),
        (f"Counts for {username[0]}", "\n".join([str(count) for count in user_count]), True)
    ])
