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
		import json
import requests

    @commands.command(aliases=['коронавирус', 'ковид'])
    async def covid(self, ctx, country):
        for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
            if item['country'] == country: 
                embed = discord.Embed(title=f'Статистика Коронавируса | {country}')
                embed.add_field(name='Выздоровело:',          value=f'{item["recovered"]} человек')
                embed.add_field(name='Заболеваний:',          value=f'{item["cases"]} человек')
                embed.add_field(name='Погибло:',              value=f'{item["deaths"]} человек')
                embed.add_field(name='Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
                embed.add_field(name='Погибло за сутки:',     value=f'+{item["todayDeaths"]} человек')
                embed.add_field(name='Проведено тестов:',     value=f'{item["tests"]} человек')
                embed.add_field(name='Активные зараженные:',  value=f'{item["active"]} человек')
                embed.add_field(name='В тяжелом состоянии:',  value=f'{item["critical"]} человек')
                embed.set_thumbnail(url=item["countryInfo"]['flag'])
                embed.set_footer(text="© Copyright 2020 хто я#0000 | Все права съедены")

                return await ctx.send(embed=embed)
def setup(Bot):
	Bot.add_cog(error(Bot))
	print("[Cog] Errors загружжен!(32 строки)")
