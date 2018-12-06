import json
import discord 
import sqlite_db as database
import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix='$')

client = discord.Client()


@bot.command()
async def get(ctx, *args):
    """Get all the counts for a user, or get the user for a specific count."""
    if (len(args) == 0):
        counts = database.get_counts_for(ctx.message.author.id)
        await ctx.send([count[0] for count in counts])
    else:
        uid = database.get_who_counted(int(args[0]))
        user = await bot.get_user_info(uid)
        await ctx.send(user.name) 

@bot.command()
async def count(ctx):
    """Count once and claim that count for the user that sent the message."""
    count = database.do_count(ctx.message.author.id)
    await ctx.send(count)

@bot.command()
async def give(ctx, user: discord.Member, count):
    """Give user the specified count if it's owned by the user that used the message."""
    if (database.get_who_counted(count) != ctx.message.author.id):
        await ctx.send("That is not your count.")
    else:
        database.give_count(user.id, count)
        await ctx.send(f"Gave {count} to {user.name}!")

if __name__ == "__main__":
    json_data = open("parameters.json")
    parameters = json.load(json_data)

    database.initialize_db()
    bot.run(parameters["token"])