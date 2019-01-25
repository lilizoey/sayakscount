import discord

async def respond(ctx, footer_text=discord.Embed.Empty,**kwargs):
    """Respond to the person that sent the message, with their name as author and avatar as pic."""
    author = ctx.message.author
    embed = discord.Embed(**kwargs, color=author.color)
    embed.set_author(name=author.name,icon_url=author.avatar_url)
    embed.set_footer(text=footer_text)
    await ctx.send(embed=embed)