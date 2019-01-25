import discord 
import db.sqlite_db as database
import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix='$')

if __name__ == "__main__":
    print("Start the bot by running start.py")