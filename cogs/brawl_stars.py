import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands



class fdvghdfbgfj(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    async def bsPlayer(self, ctx, tag= None):
        if tag == None:
            await ctx.send('Введите тэг игрока!')
        else:
            if '#' in list(tag):
                tag = tag[1:]
            
            r = requests.get(f'https://brawlace.com/players/%23{tag}')
            soup = BeautifulSoup(r.content, features= "lxml")
            stas = soup.find('table').find_all('td')

            emb = discord.Embed(
                title= soup.find('h2', {'class': 'pt-3'}).text,
                colour= discord.Color.gold()
            )
            emb.add_field(
                name= 'Максимальное кол-во трофеев',
                value= stas[1].text
            )
            emb.add_field(
                name= 'Текущее кол-во трофеев',
                value= stas[0].text
            )
            emb.add_field(
                name= 'Текущее кол-во трофеев в силовой гонке',
                value= stas[2].text
            )
            emb.add_field(
                name= 'Максимальное кол-во трофеев в силовой гонке',
                value= stas[3].text
            )
            emb.add_field(
                name= 'Уровень',
                value= soup.find('span', {'class': 'badge badge-success'}).text[6:]
            )
            emb.add_field(
                name= 'Клуб',
                value= soup.find('div', {'class': 'text-center py-3'}).find('a').text
            )
            emb.add_field(
                name= 'Попед 3 на 3',
                value= stas[4].text
            )
            emb.add_field(
                name= 'Побед дуо столкновении',
                value= stas[6].text
            )
            emb.add_field(
                name= 'Побед соло столкновении',
                value= stas[5].text
            )
            emb.set_thumbnail(
                url= soup.find('img', {'class': 'icon-medium'})['src']
            )

            await ctx.send(embed= emb)


    @commands.command()
    async def bsClan(self, ctx, clan_tag= None):
        if clan_tag == None:
            await ctx.send('Введите тэг клана!')
        else:
            if '#' in list(clan_tag):
                clan_tag = clan_tag[1:]
            
            r = requests.get(f'https://brawlace.com/clubs/%23{clan_tag}')
            soup = BeautifulSoup(r.content, features= "lxml")
            main_ = soup.find('div', {'class': 'text-center mt-2'})

            emb = discord.Embed(
                title= main_.find('h2').text,
                description= main_.find('h3').text,
                colour= discord.Color.gold()
            )
            emb.add_field(
                name= 'Глава',
                value= main_.find('a').text
            )
            emb.add_field(
                name= 'Текущее кол-во трофеев',
                value= main_.text.split('\n')[6]
            )
            emb.add_field(
                name= 'Кол-во трофеев для вступления',
                value= main_.text.split('\n')[7].replace('(', '').replace(')', '').strip()[8:]
            )
            emb.add_field(
                name= 'Участники',
                value= soup.find('h2', {'class': 'mt-3'}).text[8:].replace('(', '').replace(')', '')
            )
            emb.set_thumbnail(
                url= 'https://www.starlist.pro/assets/icon/Club.png'
            )

            await ctx.send(embed= emb)



def setup(Bot):
    Bot.add_cog(fdvghdfbgfj(Bot))
    print('[INFO] BRAWLS STARS загружен!')