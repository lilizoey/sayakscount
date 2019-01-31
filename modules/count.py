import discord
import asyncio 
import time
import typing
import discord

import modules.helpers as h

from bot import bot, database

@bot.command()
async def get(ctx, count: typing.Optional[int] = None):
    """Get all the counts for a user, or get the user for a specific count."""
    if (count is None):
        counts = [str(count[0]) for count in database.get_counts_for(ctx.message.author.id)]
        await h.respond(ctx,
            footer_text=f"that's {len(counts)} total counts.",
            title=f"These are your counts:",
            description=" ".join(counts)
        )
    else:
        uid = database.get_who_counted(count)
        user = await bot.get_user_info(uid)
        await h.respond(ctx,
            title=f"{count} has been claimed by:",
            description=f"{user.name}"
        )

@bot.command()
async def count(ctx):
    """Count once and claim that count for the user that sent the message."""
    count = database.do_count(ctx.message.author.id)
    await ctx.send(count)

@bot.command()
async def give(ctx, user: discord.Member, count: int):
    """Give user the specified count if it's owned by the user that used the message."""
    if (database.get_who_counted(count) != ctx.message.author.id):
        await ctx.send("That is not your count.")
        return
    
    database.tag_give(count, user.id)
    await ctx.send(f"{user.name}, {ctx.message.author.name} wants to give you {count}. Do you accept? type `{bot.command_prefix}accept {count}`")
    await asyncio.sleep(300)
    database.untag(ctx.message.author.id, count)

@bot.command()
async def accept(ctx, num: int):
    if (not database.check_tagged(num, ctx.message.author.id)):
        await ctx.send("Noone wants to give that to you.")
        return

    database.give_count(ctx.message.author.id, num)
    await ctx.send(f"You just got {num}!")

def cancel_give(userid, count):
    pass

def pretty_user_in_board(name, count, frac):
    percent = round(frac * 100, 2)
    return f"**{name}**: {count} {percent}%"

@bot.command()
async def lb(ctx):
    """Display the global leaderboards for who has the most counts."""
    tops = [((await bot.get_user_info(uid)).name, str(count), str(round(frac * 100, 2))) for (count, uid, frac) in database.get_top_counts()]
    (name, count, percentage) = zip(*tops)
    print
    await h.respond(ctx, title="Here are the top counters",
        fields=[
            ("Name", "\n".join([f"**{name}**" for name in name]), True),
            ("Counts", "\n".join(count), True),
            ("Percent", "\n".join([f"{percentage}%" for percentage in percentage]), True)])
