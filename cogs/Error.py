import discord
from discord.ext import commands

class error(commands.Cog):

	def __init__(self, Bot):
		self.Bot = Bot
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		ignored = commands.UserInputError

		if isinstance(error, ignored):
			return

		elif isinstance(error, commands.CommandNotFound):
			emb = discord.Embed(description = f'**:x: {ctx.author.name},Данной команды не существует.**', 
			color=0x0c0c0c)
				

			return await ctx.send(embed=emb)

		elif isinstance(error, commands.MissingPermissions):
			embed = discord.Embed(
				description="Недостаточно прав для использования данной команды",
				color=0x800080
				)
				

			return await ctx.send(embed=embed)
def setup(Bot):
	Bot.add_cog(error(Bot))
	print("[Cog] Errors загружжен!(32 строки)")