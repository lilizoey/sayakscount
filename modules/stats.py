import os
import psutil
import discord
import typing

from datetime import datetime
from bot import bot, database

import modules.helpers as h

startup = datetime.now()

INVITE = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=117760"

@bot.command()
async def invite(ctx):
    app = await bot.application_info()
    await ctx.send(INVITE.format(app.id))

@bot.command()
async def stats(ctx):
    """
    Give some stats about the bot.
    """
    app_info = await bot.application_info()

    username = f"{bot.user.name}#{bot.user.discriminator}"
    owner = f"{app_info.owner.name}#{app_info.owner.discriminator}"
    servers = bot.guilds
    channels = sum([len(server.channels) for server in servers])
    users = sum([server.member_count for server in servers])


    await h.respond(ctx, description=f"""
**Username**: {username}
**Owner**: {owner}
**Servers**: {len(servers)}
**ID**: {app_info.id}
**Library**: Discord.py {discord.__version__}
**Database Entries**: {database.get_entries()}
**Channels**: {channels}
**Users**:  {users}
**Creation Date**: {bot.user.created_at}
**Join Date**: {ctx.message.guild.me.joined_at}
**Uptime**: {datetime.now() - startup}
**Memory Usage**: {round(psutil.Process(os.getpid()).memory_info().rss / 1048576, 1)}MB
""")

@bot.command()
async def sinfo(ctx):
    server = ctx.message.guild
    owner = await bot.get_user_info(server.owner_id)
    owner_name = f"{owner.name}#{owner.discriminator}"
    voice_channels = [channel for channel in server.channels if isinstance(channel, discord.VoiceChannel)]
    text_channels = [channel for channel in server.channels if isinstance(channel, discord.TextChannel)]
    category_channels = [channel for channel in server.channels if isinstance(channel, discord.CategoryChannel)]

    msg = await h.respond(ctx, description=f"""
**{server.name}**: {server.id}
**Owner**: {owner_name}
**Region**: {str(server.region)}
**Channels**: {len(voice_channels)} voice channels, {len(text_channels)} text channels, {len(category_channels)} categories
**Members**: {server.member_count}
**Default Channel**: {server.system_channel.name if server.system_channel is not None else None}
**AFK Channel**: {server.afk_channel.name if server.afk_channel is not None else None}
**AFK Timeout**: {server.afk_timeout}
**Created On**: {server.created_at}
**Verification Requirement**: {str(server.verification_level)}
**Roles**: {", ".join([str(role).replace("@", "@​") for role in server.roles])}
**Emoji**:
""")
    for emoji in server.emojis:
        await msg.add_reaction(emoji) 

@bot.command()
async def uinfo(ctx, user: typing.Optional[discord.Member] = None):
    if (user is None):
        user = ctx.message.author 
    
    await h.respond(ctx, description=f"""
**Username:** {user.name}#{user.discriminator}
**Nick:** {user.nick}
**Status:** {user.status}
**Top Role:** {user.top_role}
**Role Color:** {user.color}
**Joined Server At:** {user.joined_at}
**Account Created At:** {user.created_at}
**User ID:** {user.id}
**User Hash:** {hash(user)}
**Avatar:** {user.avatar_url}
**Roles:** 
{",".join([str(role) for role in user.roles])}
""")