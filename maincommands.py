from discord.ext import commands
from discord.ext.commands import Context
from discord import message
import discord
import time


class MainCommands(commands.Cog):
	"""Main commands for the bot."""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="help")
	async def help(self, ctx: Context):
		"""Displays the help command."""
		embed=discord.Embed(title="Help", description="Make sure to add an * before any of these commands!", color=0xbf1212)
		embed.set_author(name="Mr. Potato", icon_url="https://yt3.ggpht.com/ytc/AKedOLSxFo9hO0XcZwSo_2LVR8xqK3KJbmY1fIMW-TF8=s900-c-k-c0x00ffffff-no-rj")
		embed.add_field(name="help", value="Displays this command", inline=True)
		embed.add_field(name="ping", value="Tests the speed of the bot.", inline=True)
		embed.add_field(name="im-bored", value="Gives you something to do.", inline=True)
		embed.add_field(name="shout <text>", value="Shouts the text", inline=True)

		embed.add_field(name="mod-help", value="View commands that only Mods can use. Requires the Mod role.", inline=True)
		message = await ctx.send(embed=embed)
		await message.add_reaction("❌")

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == "❌"
		
		reaction, user = await self.bot.wait_for("reaction_add", check=check)

		if str(reaction.emoji) == "❌":
			await message.delete()
	



	
	@commands.command(name="warn")
	@commands.has_role("Mod")
	async def warn(self, ctx: Context, member: discord.Member, *, reason: str = None):
		"""Warn a user with an optional reason."""
		await member.send(f"You have been warned on {ctx.guild} for: {reason or 'No reason given.'}")



	@commands.command(name="ping")
	async def ping(self, ctx: Context):
		"""Get the bot's current websocket latency."""
		start = time.time()
		message = await ctx.send("One moment...")
		end = time.time()
		await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end - start) * 1000)}ms")

	







class ModCommands(commands.Cog):
	"""Commands for people with the Mod tag."""

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.last_deleted_message = ""
	


	@commands.command(name="mod-help")
	@commands.has_role("Mod")
	async def mod_help(self, ctx: Context):
		"""Mod commands."""		
		
		embed = discord.Embed(title="Help", description="General help", color=0xbf1212)
		
		embed.set_author(name="Mr. Potato", icon_url="https://yt3.ggpht.com/ytc/AKedOLSxFo9hO0XcZwSo_2LVR8xqK3KJbmY1fIMW-TF8=s900-c-k-c0x00ffffff-no-rj")

		embed.add_field(name="snipe", value="Displays the command", inline=True)
		embed.add_field(name="ban <user>", value="Ban a user.", inline=False)
		embed.add_field(name="warn <user> <reason>", value="Warn a user for a reason.")

		await ctx.send(embed=embed)


		

	@commands.Cog.listener()
	async def on_message_delete(self, message: message.Message):
		self.last_deleted_message = message
	
	
	@commands.command(name="snipe")
	@commands.has_role('Mod')
	async def snipe(self, ctx: Context):
		"""A command to snipe delete messages."""
		if not self.last_deleted_message:  # on_message_delete hasn't been triggered since the bot started
			await ctx.send("There is no message to snipe!")
			return

		author = self.last_deleted_message.author
		content = self.last_deleted_message.content

		embed = discord.Embed(title=f"{author} says:", description=content)
		await ctx.send(embed=embed)
	
	@commands.command(name="ban")
	@commands.has_role("Mod")
	async def ban(self, ctx: Context, member: discord.Member):
		message = await ctx.send(f"Are you sure you want to ban {member}?")
		await message.add_reaction("✅")
		await message.add_reaction("❌")

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in "✅❌"

		try:
			reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=10)
		except: # if the mod takes more than 10 secounds to respond
			await message.edit(content="Ban cancelled because of timeout.", delete_after=5)
			await message.delete(delay=5)
			return
			
		
		if str(reaction.emoji) == "✅":
			await member.ban()
			await message.edit(content=f"{member} has been banned.")
			return
		
		await message.edit(content="Ban cancelled.", delete_after=5)
		await message.delete(delay=5)
	
	@commands.command(name="setstatus")
	@commands.cooldown(1, 20, commands.BucketType.channel)
	async def setstatus(self, ctx: Context, *, text: str):
		"""Change the bot's status. Only for people who have the Mod role."""
		await self.bot.change_presence(activity=discord.Game(name=text))



class Events(commands.Cog):
	"""Listeners."""

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.last_deleted_message = None

	
	@commands.Cog.listener()
	async def on_message(self, message: message.Message):
		if not message.guild and str(message.author) == "isaiah08#6008":
			print(message.author)
			mes = await message.reply('One moment...')
			print(message.content)
			x = input('> ')
			await mes.edit(content=x)


		
			
			
	

	@commands.Cog.listener()
	async def on_member_join(self, ctx: Context, member: discord.Member):
		await member.send(f"The potatos welcome you, {member}!")
	
	"""
	@commands.Cog.listener()
	async def on_command_error(self, ctx: Context, error:commands.CommandError):
		""Error handlers"
		if isinstance(error, commands.CommandNotFound):
			return
		elif isinstance(error, commands.CommandOnCooldown):
			message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
		elif isinstance(error, commands.MissingPermissions):
			message = "You are missing the required permissions to run this command!"
		elif isinstance(error, commands.UserInputError):
			message = "Something about your input was wrong, please check your input and try again!"
		elif isinstance(error, commands.ConversionError):
			message = "There was a conversion error. Please DM isaiah08#6008 so he can fix me!"
		else:
			message = "Oh no! Something went wrong while running the command!"
			print(error)
	


		await ctx.send(message, delete_after=5)
		await ctx.message.delete(delay=5)
	"""








def setup(bot: commands.Bot):
	bot.add_cog(MainCommands(bot))
	bot.add_cog(ModCommands(bot))
	bot.add_cog(Events(bot))

