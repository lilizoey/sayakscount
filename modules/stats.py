from bot import bot, database

INVITE = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=117760"

@bot.command()
async def invite(ctx):
    app = await bot.application_info()
    await ctx.send(INVITE.format(app.id))

@bot.command()
async def stats(ctx):
    await ctx.send(await bot.application_info())