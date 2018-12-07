import os
import psutil
import discord
from datetime import datetime
from bot import bot, database

startup = datetime.now()

INVITE = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=117760"

@bot.command()
async def invite(ctx):
    app = await bot.application_info()
    await ctx.send(INVITE.format(app.id))

@bot.command()
async def stats(ctx):
    app_info = await bot.application_info()

    username = f"{bot.user.name}#{bot.user.discriminator}"
    owner = f"{app_info.owner.name}#{app_info.owner.discriminator}"
    servers = bot.guilds
    channels = sum([len(server.channels) for server in servers])
    users = sum([server.member_count for server in servers])


    await ctx.send(f"""
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
**Memory Usage**: {str(round(float(psutil.Process(os.getpid()).memory_info().rss)/1048576, 1))+'MB'}
""")

