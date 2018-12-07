from bot import bot, database

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
    servers = len(bot.guilds)

    await ctx.send(f"""
**Username**: {username}
**Owner**: {owner}
**Servers**: {servers}
**ID**: {app_info.id}
**Library**: Discord.py rewrite
**Database Entries**: {database.get_entries()}
""")

