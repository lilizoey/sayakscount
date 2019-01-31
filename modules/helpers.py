import discord

async def respond(ctx, footer_text=discord.Embed.Empty, fields=[], **kwargs):
    """Respond to the person that sent the message, with their name as author and avatar as pic."""
    author = ctx.message.author
    embed = discord.Embed(**kwargs, color=author.color)
    embed.set_author(name=author.name,icon_url=author.avatar_url)
    embed.set_footer(text=footer_text)
    for (name, value, inline) in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)
