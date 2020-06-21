import discord,sqlite3
from discord.ext import commands


class suggest(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	db = sqlite3.connect("Suggest.db")
	cursor = db.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS suggestion(
	schannel BIGINT,
	guildid BIGINT)""")
	db.commit()
	db.close()
	
	@commands.command()
	async def suggest(self,ctx,*,sugest = None):
		if sugest == None:
			return await ctx.send("Указывайте идею обязательно") 
		db = sqlite3.connect("Suggest.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			await ctx.send("На этом сервере идеи отключены.\n Включить можно командой `suggest_set`")
		else:
			for i in cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'"):
				suggest = i[0]
				sug = self.Bot.get_channel(suggest)
				emb = discord.Embed(title=f"{ctx.message.author}",description=f"{sugest}",color =0x26bbe0)
				mesage = await sug.send(embed = emb)
				await mesage.add_reaction("✔️")
				await mesage.add_reaction("➖")
				await mesage.add_reaction("✖️")
		db.close()



	@commands.command()
	@commands.has_permissions(administrator= True)
	async def suggest_set(self,ctx,id:int):
		db = sqlite3.connect("Suggest.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			cursor.execute(f"INSERT INTO suggestion VALUES('{id}','{ctx.message.guild.id}')")
			await ctx.send("Канал для идей успешно установлен")
			db.commit()
		else:
			cursor.execute(f"UPDATE suggestion SET schannel='{id}' WHERE guildid='{ctx.message.guild.id}'")
			await ctx.send("Канал идей успешно обновлен")
			db.commit()
		db.close()
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def suggest_off(self,ctx):
		db = sqlite3.connect("Suggest.db")
		cursor = db.cursor()
		cursor.execute(f"SELECT schannel FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
		res = cursor.fetchall()
		if not res:
			return await ctx.send("На этом сервере и так отключены идеи")
		else:
			cursor.execute(f"DELETE FROM suggestion WHERE guildid='{ctx.message.guild.id}'")
			db.commit()
			await ctx.send("Идеи успешно отключены")
					
def setup(Bot):
	Bot.add_cog(suggest(Bot))
	print("[Cog] Suggest загружжен! (72 строки)")	
	