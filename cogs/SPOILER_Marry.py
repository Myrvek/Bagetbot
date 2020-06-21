import discord,sqlite3,datetime
from discord.ext import commands


class marries(commands.Cog):

	def __init__(self, Bot):
		self.Bot = Bot
	db = sqlite3.connect("Marry.db")
	cursor = db.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS marrys(
	id1 BIGINT,
    id2 BIGINT,
    datem TEXT
    )""")
	db.commit()
	db.close()

	@commands.command()
	async def marry(self, ctx, user:discord.User= None):
		db = sqlite3.connect("Marry.db") 
		cursor = db.cursor()
		no_one = []
		if user != None:
			if user == ctx.message.author:
				await ctx.send('Вы не можете жениться на себе')
			else:
				cursor.execute(f"SELECT * FROM marrys WHERE id1='{ctx.message.author.id}' OR id2='{ctx.message.author.id}'")
				res = cursor.fetchall() 
				cursor.execute(f"SELECT * FROM marrys WHERE id1='{user.id}' OR id2='{user.id}'")
				res1 = cursor.fetchall()
				if not res:
					await ctx.send(f'{user.mention}, хотите ли вы поженеться с {ctx.message.author.mention}? (Напишите : Да или Нет)')
					try:
						msg = await self.Bot.wait_for('message', timeout=300.0, check=lambda message: message.author == user)
					except asyncio.TimeoutError:
						await ctx.send('Увы, но время ожидание вышло.')
						db.close()
					else:
						if msg.content.lower() == 'да':
							cursor.execute(f"INSERT INTO marrys(id1, id2, datem) VALUES({ctx.message.author.id}, {user.id}, '{datetime.date.today()}')")
							db.commit()
							await ctx.send(f'Поздровляю! Теперь {ctx.message.author.mention} и {user.mention} женаты!')   
							db.close()
						elif msg.content.lower() == 'нет':
							await ctx.send(f'{ctx.message.author.mention}, мне жаль, но вам отказали.')
							db.close()
				else:
					if not res == no_one:
						await ctx.send('Вы уже женаты')
					elif not res1 == no_one:
						await ctx.send('Этот пользователь уже женат.')
				db.close()            
		elif user == None:
			cursor.execute(f"SELECT * FROM marrys WHERE id1='{ctx.message.author.id}' OR id2='{ctx.message.author.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send('Вы не женаты.')
				db.close()
			else:
				res = res[0]
				if res[0] == ctx.message.author.id:
					await ctx.send(f"Вы женаты с {self.Bot.get_user(res[1])}, вы женились {res[2].replace('-', '.')}")  
					db.close()
				elif res[1] == ctx.message.author.id:
					await ctx.send(f"Вы женаты с {self.Bot.get_user(res[0])}, вы женились {res[2].replace('-', '.')}")
					db.close()


	@commands.command()
	async def divorce(self, ctx):
		db = sqlite3.connect("Marry.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM marrys WHERE id1='{ctx.message.author.id}' OR id2='{ctx.message.author.id}'")
		res = cursor.fetchall()
		if not res:
			await ctx.send('Вы не женаты.')
			db.close()
		else:
			await ctx.send(f'Вы точно хотите развестись?(Напишите : Да или Нет)')
			try:
				msg = await self.Bot.wait_for('message', timeout=10.0, check=lambda message: message.author == ctx.author)
			except asyncio.TimeoutError:
				await ctx.send('Увы, но время ожидание вышло.')
				db.close()
			else:
				if msg.content.lower() == 'да':
					cursor.execute(f"DELETE FROM marrys WHERE id1='{ctx.message.author.id}' OR id2='{ctx.message.author.id}'")
					db.commit()
					db.close()
					await ctx.send('Вы развелись.')
				elif msg.content.lower() == 'нет':
					await ctx.send('Вы отменили команду.')
					db.close()


def setup(Bot):
	Bot.add_cog(marries(Bot))
	print('[Cog] Marry загружжен!')