import discord

async def respond(ctx, footer_text=discord.Embed.Empty,**kwargs):
    embed = discord.Embed(**kwargs)
    author = ctx.message.author
    embed.set_author(name=author.name,icon_url=author.avatar_url)
    embed.set_footer(text=footer_text)
    await ctx.send(embed=embed)