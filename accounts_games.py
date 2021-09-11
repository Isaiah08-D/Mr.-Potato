from discord.ext import commands
from discord.ext.commands import Context
from discord import message
import discord
import time
from replit import db
import requests
from json import loads


class FunCommands(commands.Cog):
	"""Fun commands, including API stuff."""

	def __init__(self, bot: commands.Bot):
		self.bot = bot
	

	@commands.command(name="im-bored")
	async def bored(self, ctx: Context):
		"""Returns something to do."""

		if str(ctx.author) in db:
			db[str(ctx.author)]['usage'] += 1
		else:
			db[str(ctx.author)] = {'usage': 1, 'points': 0, 'servers': [str(ctx.guild)]}

		if str(ctx.guild) not in db[str(ctx.author)]['servers']:
			db[str(ctx.author)]['servers'].append(str(ctx.guild))
		

		message = await ctx.send("One moment..."
		)
		req = requests.get("http://www.boredapi.com/api/activity?price=0.0")
		if req.status_code == 200:
			req = loads(req.text)
			embed = discord.Embed(
				title="Why not you...",
				description=str(req["activity"])
			)
			await message.edit(content="", embed=embed)
	
	@commands.command(name="shout")
	async def shout(self, ctx: Context, *, message: str):
		"""Shout a message."""


		
		if str(ctx.author) in db:
			db[str(ctx.author)]['usage'] += 1
		else:
			db[str(ctx.author)] = {'usage': 1, 'points': 0, 'servers': [str(ctx.guild)]}

		if str(ctx.guild) not in db[str(ctx.author)]['servers']:
			db[str(ctx.author)]['servers'].append(str(ctx.guild))



		embed = discord.Embed(
			title=f"{str(ctx.author)} says:",
			description=message
		)

		await ctx.send(embed=embed)

class Accounts(commands.Cog):
	"""Account info"""

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command('me')
	async def me(self, ctx: Context):
		user_info = db[str(ctx.author)]

		embed=discord.Embed(
			title=str(ctx.author),
			description="",
			color=0xbf1212
		)
		embed.set_author(
			name="Mr. Potato", 	
			icon_url="https://yt3.ggpht.com/ytc/AKedOLSxFo9hO0XcZwSo_2LVR8xqK3KJbmY1fIMW-TF8=s900-c-k-c0x00ffffff-no-rj"
		)

		servers = ''
		for server in user_info['servers']: servers += server + ', '

		embed.add_field(name="Usage", value=str(user_info['usage']), inline=True)
		embed.add_field(name="Points", value=str(user_info['points']), inline=True)
		embed.add_field(name="Servers", value=servers[:-2], inline=True)

		await ctx.send(embed=embed)
	
	@commands.command('status')
	async def status(self, ctx: commands.Context, *, member: discord.Member):
		try:
			user_info = db[str(member)]
		except KeyError:
			message = await ctx.send("That user either hasn't used this bot or doesn't exist!", delete_after=5)
			await message.delete(delay=5)

		embed=discord.Embed(
			title=str(ctx.author),
			description="",
			color=0xbf1212
		)
		embed.set_author(
			name="Mr. Potato", 	
			icon_url="https://yt3.ggpht.com/ytc/AKedOLSxFo9hO0XcZwSo_2LVR8xqK3KJbmY1fIMW-TF8=s900-c-k-c0x00ffffff-no-rj"
		)

		servers = ''
		for server in user_info['servers']: servers += server + ', '

		embed.add_field(name="Usage", value=str(user_info['usage']), inline=True)
		embed.add_field(name="Points", value=str(user_info['points']), inline=True)
		embed.add_field(name="Servers", value=servers[:-2], inline=True)

		await ctx.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(FunCommands(bot))
	bot.add_cog(Accounts(bot))