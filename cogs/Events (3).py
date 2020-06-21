import discord,sqlite3
from discord.ext import commands
sqlite_event ='DB/Event.db'

class database():
	def connection():
		db = sqlite3.connect(sqlite_event)
		return db
	


class Event(commands.Cog):

	def __init__(self, Bot):
		self.Bot = Bot
	mydb = database.connection()
	cursor = mydb.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS joins(
		message TEXT,
		channel BIGINT,
		guildid BIGINT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS leave(
		message TEXT,
		channel BIGINT,
		guildid BIGINT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS autorole(
		role BIGINT,
		guildid BIGINT)""")
	mydb.commit()
	mydb.close()
	@commands.Cog.listener()
	async def on_member_join(self,member):
		mydb = database.connection()
		cursor = mydb.cursor()
		cursor.execute(f"SELECT channel FROM joins WHERE guildid='{member.guild.id}'")
		res = cursor.fetchall()
		if not res:
			pass
		else:
			for i in res:
				channel = i[0]
				message_channel = self.Bot.get_channel(channel)
				for i in cursor.execute(f"SELECT message FROM joins WHERE guildid='{member.guild.id}'"):
					message = i[0]
					await message_channel.send(f"{message}")
				cursor.execute(f"SELECT role FROM autorole WHERE guildid='{member.guild.id}'")
				res2 = cursor.fetchall()
				if not res2:
					pass
				else:
					for i in res2: 
						autorole = i[0]
						role = discord.utils.get( member.guild.roles, id = autorole )
						await member.add_roles(role)

		mydb.close()
	@commands.command()
	@commands.has_permissions(administrator= True)
	async def join(self,ctx,arg: str=None,channel:discord.TextChannel=None,*,message=None):
		mydb = database.connection()
		cursor = mydb.cursor()

		if arg == "enable":
			if channel==None:
				return await ctx.send("Указывайте канал обязательно!!!")
			cursor.execute(f"SELECT channel FROM joins WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				cursor.execute(f"INSERT INTO joins VALUES('{message}','{channel.id}','{ctx.message.guild.id}')")
				await ctx.send("Канал для сообщений о заходе успешно установлен")
			else:
				cursor.execute(f"UPDATE joins SET channel='{channel.id}',message='{message}'WHERE guildid='{ctx.message.guild.id}'")
				await ctx.send("Канал для сообщений о заходе успешно обновлен")
		elif arg == "disable":

			cursor.execute(f"SELECT channel FROM joins WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()

			if not res:
				await ctx.send("На этом сервере не настроены сообщения о заходе!")
			else:
				cursor.execute(f"DELETE FROM joins WHERE guildid='{ctx.message.guild.id}'")
				await ctx.send("Сообщения о заходе успешно отключены")
		mydb.commit()
		mydb.close()
	@commands.command()
	async def check_test(self,ctx):
		mydb = database.connection()
		cursor = mydb.cursor()
		res = cursor.execute(f"SELECT * FROM autorole WHERE guildid='{ctx.message.guild.id}'")
		for i in res:
			await ctx.send(f"{i}")
	@commands.command()
	@commands.has_permissions(administrator= True)
	async def autorole(self, ctx, arg: str=None, role: discord.Role= None):
		if arg == None:
			await ctx.send("enable — включить автороль.\ndisable — отключить автороль.")
			return
		mydb = database.connection()
		cursor = mydb.cursor()
		if arg == "enable":
			if role == None:
				await ctx.send("Обязательно указывайте автороль.")
				return
			cursor.execute(f"SELECT role FROM autorole WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				cursor.execute(f"INSERT INTO autorole VALUES('{role.id}','{ctx.message.guild.id}')")
				await ctx.send("Автороль успешно установлена.")
			else:
				cursor.execute(f"UPDATE autorole SET role='{role.id}' WHERE guildid='{ctx.message.guild.id}' ")
				await ctx.send("Автороль успешно обновлена!")
		elif arg == "disable":
			cursor.execute(f"SELECT role FROM autorole WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send("Автороль и так отключена.")
				return
			else:
				cursor.execute(f"DELETE FROM autorole WHERE guildid='{ctx.message.guild.id}'")
				await ctx.send("Автороль успешно отключена.")
		mydb.commit()
		mydb.close()

	@commands.command()
	@commands.has_permissions(administrator= True)
	async def leave(self, ctx, arg: str= None, channel:discord.TextChannel = None, text: str= None):
		mydb = database.connection()
		cursor = mydb.cursor()
		print(arg)

		if arg == None:
			return await ctx.send("enable— установить канал сообщений о выходе.\ndisable— отключить канал сообщений о выходе.")


		if arg == "enable":
			cursor.execute(f"SELECT channel FROM leave WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				cursor.execute(f"INSERT INTO leave VALUES('{text}','{channel.id}','{ctx.message.guild.id}')")
				await ctx.send("Канал для сообщений о выходе  успешно установлен!!")
			else:
				cursor.execute(f"UPDATE leave SET channel='{channel.id}',message='{text}'WHERE guildid='{ctx.message.guild.id}'")
				await ctx.send("Канал для сообщений об выходе успешно обновлен!")
		elif arg == "disable":
			cursor.execute(f"SELECT channel FROM leave WHERE guildid='{ctx.message.guild.id}'")
			res = cursor.fetchall()
			if not res:
				await ctx.send("Канал для сообщений об выходе и так отключен")
			else:
				cursor.execute(f"DELETE FROM leave WHERE guildid='{ctx.message.guild.id}'")
				await ctx.send("Канал для сообщений об выходе успешно отключен")
		mydb.commit()
		mydb.close()
	@commands.Cog.listener()
	async def on_member_remove(self,member):
		mydb = database.connection()
		cursor = mydb.cursor()
		cursor.execute(f"SELECT channel FROM leave WHERE guildid='{member.guild.id}'")
		res = cursor.fetchall()
		if not res:
			pass
		else:
			for i in res:
				channel =i[0]
				leave_channel = self.Bot.get_channel(channel)
				for i in cursor.execute(f"SELECT message FROM leave WHERE guildid='{member.guild.id}'"):
					message = i[0]
					await leave_channel.send(f"{message}")

def setup(Bot):
	Bot.add_cog(Event(Bot))
	print("[Cog] Event загружжен!")		
		