import discord,sqlite3
from discord.ext import commands

class report(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	db = sqlite3.connect("Report.db")
	cursor = db.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS report(
	rchannel BIGINT,
	guildid BIGINT)""")


	@commands.command()
	async def report(self,ctx,*,report=None):
		if report == None:
			return await ctx.send("Указывайте жалобу обязательно")
		db = sqlite3.connect("Report.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT rchannel FROM report WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			return await ctx.send("На этом сервере не установлен канал для жалоб \n Установить можно при помощи команды`report_set`")
		else:
			for rchannel in cursor.execute(f"SELECT rchannel FROM report WHERE guildid='{ctx.message.guild.id}'"):
				channel = rchannel[0]
				repchannel = self.Bot.get_channel(channel)
				emb = discord.Embed(title=f"Жалоба от {ctx.message.author.name}",description =f"{report}",color=0xdb5318)
				await repchannel.send(embed = emb)
				db.close()

	@commands.command()
	@commands.has_permissions(administrator= True)
	async def report_set(self,ctx,id:int):
		if not id:
			return await ctx.send(":x:Обязательно укажите канал для репортов!",delete_after=5)
		db = sqlite3.connect("Report.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT rchannel FROM report WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			cursor.execute(f"INSERT INTO report VALUES('{id}',{ctx.message.guild.id}) ")
			await ctx.send("Канал для жалоб успешно установлен!!!")
			db.commit()
			
		else:
			cursor.execute(f"UPDATE report SET rchannel='{id}'WHERE guildid='{ctx.message.guild.id}'")
			await ctx.send("Канал для жалоб обновлен")
			db.commit()
		db.close()
	@commands.command()
	@commands.has_permissions(administrator= True)
	async def report_off(self,ctx):
		db = sqlite3.connect("Report.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT rchannel FROM report WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			return await ctx.send("Жалобы и так отключены")
		else:
			cursor.execute(f"DELETE FROM report WHERE guildid='{ctx.message.guild.id}'")
			await ctx.send("Жалобы успешно отключены!")
			db.commit()
			db.close()






def setup(Bot):
	Bot.add_cog(report(Bot))
	print("[Cog] Report загружжен!(74 строки)")	