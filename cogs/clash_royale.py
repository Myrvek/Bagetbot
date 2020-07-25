import discord
import requests
from bs4 import BeautifulSoup
from .imports.override import check_channel_override
from discord.ext import commands



class fdfdfsdvfvs(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @check_channel_override()
    async def crPlayer(self, ctx, tag= None):
        if tag == None:
            await ctx.send('Введите тэг игрока!')
        else:
            if '#' in list(tag):
                tag = tag[1:]
            
            r = requests.get(f'https://statsroyale.com/profile/{tag}')

            soup = BeautifulSoup(r.content, features="lxml")
            stats = soup.find_all('div', {'class': 'statistics__metricCounter ui__headerExtraSmall'})
            deck = soup.find('div', {'class': 'profile__currentDeckList'})
            cards_names = deck.find_all('img')
            chests = soup.find('div', {'class': 'chests__queue'})


            curent_deck = ', '.join([card['src'].split('/')[6][:-4] for card in cards_names])

            emb = discord.Embed(
                title= ''
            )
            emb.add_field(
                name= f'Максимальное кол-во трофеев',
                value= stats[0].text
            )
            emb.add_field(
                name= f'Текущее кол-во трофеев',
                value= stats[1].text
            )
            if int(stats[1].text) > 4000:
                emb.add_field(
                    name= f'Лига',
                    value= stats[21].text
                )
            emb.add_field(
                name= f'Победы',
                value= stats[2].text
            )
            emb.add_field(
                name= f'Проигрыши',
                value= stats[3].text
            )
            emb.add_field(
                name= f'Карт задоначено',
                value= stats[5].text
            )
            emb.add_field(
                name= 'Любимая карта',
                value= soup.find('span', {'class': 'profile__favouriteCardName'}).text
            )
            emb.add_field(
                name= 'Колода',
                value= curent_deck
            )

            await ctx.send(embed= emb)


    @commands.command()
    @check_channel_override()
    async def crClan(self, ctx, clan_tag= None):
        if clan_tag == None:
            await ctx.send('Введите тэг клана!')
        else:
            if '#' in list(clan_tag):
                clan_tag = clan_tag[1:]
            
            r = requests.get(f'https://statsroyale.com/clan/{clan_tag}?fresh=1')

            soup = BeautifulSoup(r.content, features="lxml")
            clan_info = soup.find('div', {'class': 'clan__name'})
            clan_static = soup.find('div', {'class': 'clan__statistics'})
            troph = clan_static.find_all('div', {'class': 'clan__metric clan__trophyMetric'})

            emb = discord.Embed(
                title= clan_info.find('div', {'class': 'ui__headerMedium clan__clanName'}).text,
                description= clan_info.find('div', {'class': 'ui__mediumText'}).text,
                colour= discord.Color.green()
            )
            emb.add_field(
                name= 'Текущее кол-во трофеев',
                value= troph[0].find('div', {'class': 'ui__headerMedium'}).text
            )
            emb.add_field(
                name= 'Кол-во трофеев для вступления',
                value= troph[1].find('div', {'class': 'ui__headerMedium'}).text
            )
            emb.add_field(
                name= 'Донат карт за неделю',
                value= clan_static.find('div', {'class': 'clan__metric clan__donationsMetric'}).find('div', {'class': 'ui__headerMedium'}).text
            )
            emb.add_field(
                name= 'Трофеи в КВ',
                value= clan_static.find('div', {'class': 'clan__metric clan__clanWarsMetric'}).find('div', {'class': 'ui__headerMedium'}).text
            )
            emb.set_thumbnail(
                url= clan_info.find('img')['src']
            )

            await ctx.send(embed= emb)



def setup(Bot):
    Bot.add_cog(fdfdfsdvfvs(Bot))
    print('[INFO] CLASH ROYALE загружен!')