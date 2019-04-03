import discord
import typing
from bot import bot, database

class Trade():
    """
    Representing a trade between two people.
    """
    def __init__(self, trader1, trader2):
        self.traders = [trader1, trader2]
        self.counts = [{}, {}]

    def which_user(self, id):
        """
        Figuring out which user the id corresponds to
        """
        for i in range(0, len(self.traders)):
            if self.traders[i].id == id:
                return i
        
        return None

    def add_number(self, count):
        """
        Add a number to the trade if it belogns to one 
        of the traders.
        """
        count_id = database.get_who_counted(count)
        trader_index = self.which_user(count_id)

        if trader_index is None:
            return False
        
        self.counts[trader_index].add(count)
        return True
    
    def __str__(self):
        s = ""
        for i in range(0, len(self.traders)):
                s += self.traders[i].name
                s += "\t" + str(self.counts[i])

        return s

    def execute(self):
        """
        Perform the trade, swapping all numbers between users.
        """
        print("WARNING, not exchanging as a transaction!")
        for i in range(0, len(self.traders)):
            for count in self.counts[i]:
                database.give_count(self.traders[i].id, count)

@bot.command()
async def trade(ctx, user: discord.Member):
    trade_obj = Trade(ctx.message.author, user)
    quit = False
    await ctx.send("test")

    while not quit:
        def check(msg):
            print(trade_obj.which_user(msg.author.id))
            return trade_obj.which_user(msg.author.id) is not None and msg.channel.id == ctx.message.channel.id

        msg = await bot.wait_for("message", check=check)
        if msg.content == "quit":
            quit = True
            continue
        
        try:
            count = int(msg.content)
            trade_obj.add_number(count)
            await ctx.send(str(trade_obj))
        except ValueError as e:
            pass


