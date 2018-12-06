import json

from modules import *
from bot import bot, database

if __name__ == "__main__":
    json_data = open("parameters.json")
    parameters = json.load(json_data)

    database.initialize_db()
    bot.run(parameters["token"])