from discord.ext import commands
import discord
import os
import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="*")

bot.remove_command("help")
bot.remove_command("warn")



bot.load_extension("maincommands") 
bot.load_extension("accounts_games")



keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))
