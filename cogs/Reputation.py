import discord,sqlite3
from discord.ext import commands
sqlite_rep = 'DB/Rep.db'
class database():
	def connection():
		db = sqlite3.connect(sqlite_rep)
		return db

class Rep(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	mydb = database.connection()
	cursor = mydb.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS users(
		rep INT,
		id BIGINT)""")
	mydb.commit()
	mydb.close()

	@commands.command(aliases = ['my_thx', 'rep-me'])
	async def my_rep(self, ctx, member: discord.Member = None):
		mydb = database.connection()
		cursor = mydb.cursor()
		if member is None:
			cursor.execute(f"SELECT rep FROM users WHERE id ='{ctx.message.author.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send(embed = discord.Embed(
						description = f'У **{ctx.author}** нету благодарностей. '
					))
			else:
				for i in res:
					rep = i[0]
					await ctx.send(embed = discord.Embed(
						description = f'У **{ctx.author}** {rep} благодарностей. '
					))
		else:
			cursor.execute(f"SELECT rep FROM users WHERE id = {member.id}")
			res = cursor.fetchall()
			if not res:
				await ctx.send(embed = discord.Embed(
					description = f'У **{member.name}** нету благодарностей. '
				))
			else:
				cursor.execute(f"SELECT rep FROM users WHERE id = {member.id}")
				res = cursor.fetchall()
				for i in res:
					rep = i[0]
					if rep == 1: 
						await ctx.send(embed = discord.Embed(
						description = f'У **{member}** {rep} благодарность'
					))
					else:
						await ctx.send(embed = discord.Embed(
							description = f'У **{member}** {rep} благодарностей'
						))
		mydb.commit()
		mydb.close()

	@commands.command(aliases = ['rep',  'thank'])
	async def thx(self, ctx, member: discord.Member = None):
		mydb = database.connection()
		cursor = mydb.cursor()
		if member is None:
			await ctx.send(embed = discord.Embed(
				description = f' **{ctx.author}**, укажите пользователя, которому хотите отправить благодарность'
			))
		else:
			if member.id == ctx.author.id:
				await ctx.send(f'**{ctx.author}**, нельзя выдавать благодарности самому себе!')
			else:
				cursor.execute(f"SELECT rep FROM users WHERE id  = '{member.id}'")
				res = cursor.fetchall()
				if not res:
					cursor.execute(f"INSERT INTO users VALUES('{1}','{member.id}')")
					await ctx.message.add_reaction('✔️')
				else:					
					for i in res:
						rep = i[0]
						cursor.execute(f"UPDATE users SET rep = '{rep + 1}' WHERE id = {member.id}")
						await ctx.message.add_reaction('✔️')
		mydb.commit()
		mydb.close()
	@commands.command()
	async def test(self, ctx):
		mydb = database.connection()
		cursor = mydb.cursor()
		for i in cursor.execute("SELECT * FROM users"):
			return i
		mydb.close()

def setup(Bot):
	Bot.add_cog(Rep(Bot))
	print('[Cog] Rep загружжен!')
