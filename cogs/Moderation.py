import discord,sqlite3
from discord.ext import commands

class moderation(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	@commands.command( 
		pass_context = True, aliases=[ "Мут", "мут", "мьют", "Мьют", "Mute" ] 
	)
	@commands.has_permissions(
		manage_roles = True
	)
	async def mute(self, ctx, member : discord.Member, * , arg: str ):

		if member == ctx.message.author:
			return await ctx.send("Ты не можешь замьютить **сам себя**!",delete_after=5)

		sendmute = f'**Вы были замучены на сервере {ctx.guild.name} на по причине: {arg}**'
		mute_role = discord.utils.get( ctx.message.guild.roles, name = "Muted" )

		if not mute_role:
			await ctx.guild.create_role(name = "Muted")

		if mute_role in member.roles:
			await ctx.send(embed = discord.Embed(description = f'**:warning: Данный пользователь {member.mention} уже замьючен!**', color=0x800080))

		else:
			await member.add_roles(mute_role, reason=None, atomic=True)
			await ctx.send(embed = discord.Embed(description = f'**:shield:Мут пользователю {member.mention} успешно выдан по причине: {arg}**', color=0x0000FF))
			await member.send(embed = discord.Embed(description = f'{sendmute}', color=0x0c0c0c))
	

	@mute.error 
	async def mute_error(self, ctx, error):

		if isinstance( error, commands.MissingPermissions):
			await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

		if isinstance( error, commands.MissingRequiredArgument): 
			await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите юзера!.**', color=0x0c0c0c))

	@commands.command( pass_context = True, aliases=[ "Размут", "размут", "размьют", "Разьют", "Unmute" ] )
	@commands.has_permissions(manage_roles = True)

	async def unmute(self, ctx, member : discord.Member):

		mute_role = discord.utils.get( ctx.message.guild.roles, name = "Muted" )

		if mute_role in member.roles:
			sendunmute = f'**Вы были размучены на сервере {ctx.guild.name}**'
			
			await member.remove_roles( mute_role )
			await ctx.send(embed = discord.Embed(description = f'**:white_check_mark:Мут у пользователя {member.mention} успешно снят!:white_check_mark:**', color=0x800080))
			await member.send(embed = discord.Embed(description = f'{sendunmute}', color=0x800080))
		else:
			await ctx.send(embed = discord.Embed(description = f'**:warning: Данный пользователь {member.mention} не замьючен!**', color=0x800080))
	
	@commands.command(name='ban')
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member=None, *, reason=None):
		if not member:
			await ctx.send("Укажите юзера")
		if ctx.author.top_role.position < member.top_role.position:
			return await ctx.send('Ehm... Это троллинг или что? ')
		if member.id == ctx.message.author.id or member.id == ctx.message.guild.me.id:
			await ctx.send('Ты не можешь банить роли или себя')
			return
		if member.top_role.position >= ctx.message.guild.me.top_role.position:
			await ctx.send('Он выше меня!')
			return
		if not reason:
			reason = 'None'
		else:
			reason = reason

		embed = discord.Embed(title='Делаю', description='Вы хотите забанить {} по причине `{}` \n если вы согласны нажмите :white_check_mark:'.format(member.name, reason))
		embed.color = 0x32a852

		message = await ctx.send(embed=embed)
		await message.add_reaction(':white_check_mark:')
		await message.add_reaction(':negative_squared_cross_mark:')
		try:
			r, u = await self.bot.wait_for('reaction_add', check=lambda r,u: u.id == ctx.message.author.id, timeout=60)
		except asyncio.TimeoutError as e:
			await ctx.send('Время вышло')
		else:
			if str(r) == ':white_check_mark:':
				await member.send(f"Вы были забанены в  {ctx.guild.name} по причине {reason} от {ctx.author.name}")
				await ctx.message.guild.ban(member, reason=reason, delete_message_days=7)
				await ctx.send('Я забанил {} по причине `{}` '.format(f'<@{member.id}>', reason))
			else:
				await ctx.send('Отмена')
				return
	@commands.command()
	@commands.has_permissions(administrator= True)
	async def unban(self,ctx,*,member):
		await ctx.message.delete()
		banned_users = await ctx.guild.bans()
		emb =discord.Embed(title)

		for ban_entry in banned_users:
			user = ban_entry.user
			await ctx.guild.unban(user)
			await ctx.send(f"{member.name} Был разбанен!")
			return
	@commands.command()
	@commands.has_permissions(kick_members= True)
	async def kick(self,ctx,member: discord.Member,*,reason = None):
		if member == ctx.message.author:
			return await ctx.send("Ты не можешь кикнуть сам себя.")
		await ctx.message.delete()
		embed = discord.Embed(title = f"Ты был кикнут {member.name}!",
			color=0x00ff80,
			description ="Сервер:"f"{ctx.message.guild}"f"\nМодератор:{ctx.message.author.mention}\nПричина:{reason} "
			 )
		embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
	@commands.command()
	@commands.has_permissions(manage_messages= True)
	async def clear(self,ctx,amount=100):
		await ctx.channel.purge(limit=amount + 1)

	


def setup(Bot):
	Bot.add_cog(moderation(Bot))
	print("[Cog] Moderation загружжен!(128 строки)")