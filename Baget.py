# -*- coding: utf8 -*-

import discord 
from discord.ext import commands 
import datetime
import nekos 
import asyncio
import wikipedia
import pyowm
import os
from discord import utils
from discord.ext.commands import Bot
import re
import json
import sqlite3
import io
import requests
import random 
import time
from Cybernator import Paginator



Bot = commands.Bot(command_prefix='b_') # Переменная бота, тут вводите префикс какой вы хотите
Bot.remove_command('help') 



for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        Bot.load_extension(f'cogs.{file[:-3]}')

def postfix(num:int, end_1:str='год', end_2:str='года', end_3:str='лет'): # Функция обработрки постфикса
    num = num % 10 if num > 20 else num # Делим число на 10 и получаем то что осталось после деления, дальше проверка это больше чем 20 или нет, если больше то оставляем число не изменныс, а если меньше то заменяем число на остаток деления
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3 # Тут уже просто прлверяем



@Bot.event
async def on_ready():
    while True:
        await Bot.change_presence(activity= discord.Activity(name=' на жизнь', type= discord.ActivityType.watching))
        await asyncio.sleep(10)
        await Bot.change_presence(activity= discord.Game("Команда помощи b_help"))
        await asyncio.sleep(10)
        await Bot.change_presence(activity= discord.Game("Создан Baget.Co"))
        await asyncio.sleep(10)


       

print("[Cog] Other (498 строк)")
print("[Main File] Главный фаил был загружен")
    

        
@Bot.command()
async def vote(ctx):
    emb = discord.Embed(
        title= 'Проголосовать за бота вы можете тут'
    )
    emb.add_field(
        name= 'top.gg',
        value= '[Ссылка](https://top.gg/bot/702555544480645191/vote)'
    )
    await ctx.send(embed=emb)

@Bot.command() # Декоратор команды
async def avatar(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # Проверка аргуменат и переменная участника
    emb = discord.Embed( # Переменная ембеда
        title=f'Аватар пользователя {user}', # Заполняем заголовок
        description= f'[Ссылка на изображение]({user.avatar_url})', # Запонлняем описание
        color=user.color # Устанавливаем цвет
    )
    emb.set_image(url=user.avatar_url) # Устанавливаем картинку
    await ctx.send(embed=emb) # Отпрвака ембеда
#Work 
   
@Bot.command() # Декоратор команды
async def servercount(ctx): # Название команды
    await ctx.send(f'Бот есть на {len(Bot.guilds)} серверах') # Выводит кол-во серверов бота

@Bot.command()
async def stats(ctx):
    emb = discord.Embed(title = "**Статистика бота **",color = 0x29f1ff)
    emb.add_field(name = "Команд", value = f"{len(ctx.bot.commands)}")
    emb.add_field(name = "Возраст", value =f"{(datetime.datetime.now() - ctx.bot.user.created_at).days} дней" )
    emb.add_field(name = "Серверов",value=f"{len(self.Bot.guilds)} сервер")
    emb.add_field(name = "Юзеры", value=f"{len(self.Bot.users)}")
    emb.add_field(name = "Эмодзи", value = f"{len(self.Bot.emojis)}")
    await ctx.send(embed = emb)

@Bot.command()
async def knb(ctx):
    solutions = ['✂️', '🧱', '📄']
    winner = "**НИЧЬЯ**"
    msg = await ctx.send('Выберите ход :')
    for r in solutions:
        await msg.add_reaction(r)
    try:
        react, user = await Bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in solutions)
    except asyncio.TimeoutError:
        await ctx.send('Время вышло')
        await msg.delete()
        await ctx.message.delete()
    else:
        p1 = solutions.index(f'{react.emoji}')
        p2 = random.randint(0, 2)
        if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
            winner = f"{ctx.message.author.mention} ты **Проиграл**"
        elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
            winner = f"{ctx.message.author.mention} ты **Выиграл**"
        await ctx.send(    
            f"{ctx.message.author.mention} **=>** {solutions[p1]}\n"
            f"{Bot.user.mention} **=>** {solutions[p2]}\n"
            f"{winner}")
        await msg.delete()
        await ctx.message.delete()
#work

@Bot.command() # Декоратор команды
async def ping(ctx): # # Название команды
    emb = discord.Embed( # Переменная ембеда
        title= 'Текущий пинг', # Заполняем заголовок
        description= f'{Bot.ws.latency * 1000:.0f} ms' # Запонлняем описание
    )
    await ctx.send(embed=emb) # Отпрвака ембеда 

#work

@Bot.command() # Декоратор команды
async def ran_avatar(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.') # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда
#work

@Bot.command() # Декоратор команды
async def ran_color(ctx): # Название команды
    clr = (random.randint(0,16777215)) # Генерируем рандомное число от 0 до 16777215, это нужно чтобы сделать цвет
    emb = discord.Embed( # Переменная ембеда
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``', # Jписание ембеда, и код с помощью которого мы делаем цвет
        colour= clr # Устанавливаем цвет ембеду
    )

    await ctx.send(embed=emb) # Отпрвака ембед
#work

@Bot.command() # Декоратор команды
async def kiss(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете поцеловать сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('kiss')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед
#work
        
@Bot.command() # Декоратор команды
async def hug(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед
#work
        
@Bot.command() # Декоратор команды
async def slap(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете ударить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед
#work
        
@Bot.command() # Декоратор команды
async def pat(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете погладить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
        emb.set_image(url=nekos.img('pat')) # Ищем картинку и ставим её в ембед

        await ctx.send(embed=emb) # Отпрвака ембед


@Bot.command() # Декоратор команды
async def profile(ctx, userf: discord.Member = None): # Название команды и аргумент
    user = ctx.message.author if userf == None else userf # Проверка указан ли пользователь, если нет то заменяем автором команды
    status = user.status # Получаем статус

    if user.is_on_mobile() == True: stat = 'На телефоне' # Проверка статуса и указываем статус
    if status == discord.Status.online: stat = 'В сети' # Проверка статуса и указываем статус
    elif status == discord.Status.offline: stat = 'Не в сети' # Проверка статуса и указываем статус
    elif status == discord.Status.idle: stat = 'Не активен' # Проверка статуса и указываем статус
    elif status == discord.Status.dnd: stat = 'Не беспокоить' # Проверка статуса и указываем статус

    create_time = (datetime.datetime.today()-user.created_at).days # Узнаем кол-во дней в дискорде
    join_time = (datetime.datetime.today()-user.joined_at).days # Узнаем кол-во дней на сервере

    emb = discord.Embed(title='Профиль', colour= user.color) # Делаем ембед и устанавливаем цвет
    emb.add_field(name= 'Ник', value= user.display_name, inline= False) # Добавляем поле и заполняем 
    emb.add_field(name= 'ID', value= user.id, inline= False) # Добавляем поле и заполняем 
    
    if create_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни в дискорде
    else:
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( {create_time} {postfix(create_time, "день", "дня", "дней")})', inline= False)# Добавляем поле и заполняем кол-во дней в дискорде и подбираем окончание
    if join_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни на сервере
    else:
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( {join_time} {postfix(join_time, "день", "дня", "дней")} )', inline= False) # Добавляем поле и заполняем кол-во дней на сервере и подбираем окончание
    emb.add_field(name= 'Наивысшая роль', value= f"<@&{user.top_role.id}>", inline= False) # Добавляем поле и заполняем роль
    emb.add_field(name= 'Статус', value= stat, inline= False) # Добавляем поле и заполняем статус
    emb.set_thumbnail(url= user.avatar_url) # Устанавливаем картинку сбоку ( В душе хз как назвать xD )

    await ctx.send(embed=emb) 

@Bot.command() # Декоратор, показывает коду что это команда
async def hello(ctx): # Функция и название функции, то есть, название команды
    await ctx.send(f'{ctx.message.author.mention}, Hey bro nice day).') # Ответ бота заданым текстом

def random_meme():
    with open('memes_data2.txt', 'r') as file:
        memes = file.read().split(',')
    picked_meme = random.choice(memes)
    return picked_meme
@Bot.command()
async def man(ctx):
    emb = discord.Embed()
    emb.set_image(url= random_meme())
    await ctx.send(embed=emb)
owm = pyowm.OWM('9963f6627710292d5125e8200fc5b2b5', language= 'ru')
@Bot.command()
async def wea(ctx, *, arg):
    observation = owm.weather_at_place(arg)
    w = observation.get_weather()
    prs = w.get_pressure()
    tmp = w.get_temperature('celsius')
    hmd = w.get_humidity()
    cld = w.get_clouds()
    wnd = w.get_wind()
    wnds = wnd.get('speed')
    wnds_str = ''
    rn = w.get_rain()
    emb = discord.Embed(
        title= 'Текущая погода'
    )
    emb.add_field(
        name= 'Температура',
        value= f'{tmp.get("temp")}°'
    )
    emb.add_field(
        name= 'Давление',
        value= str(prs.get('press')) + 'мм рт.ст.'
    )
    emb.add_field(
        name= 'Влажность',
        value= str(hmd) + '%'
    )
    emb.add_field(
        name= 'Облачность',
        value= str(cld) + '%'
    )
    if wnds < 0.2:wnds_str = 'Штиль'
    elif wnds < 1.5: wnds_str = 'Тихий'
    elif wnds < 3.3: wnds_str = 'Лёгкий'
    elif wnds < 5.4: wnds_str = 'Слабый'
    elif wnds < 7.9: wnds_str = 'Умеренный'
    elif wnds < 10.7: wnds_str = 'Свежий'
    elif wnds < 13.8: wnds_str = 'Сильный'
    elif wnds < 17.1: wnds_str = 'Крепкий'
    elif wnds < 20.7: wnds_str = 'Очень крепкий'
    elif wnds < 24.4: wnds_str = 'Шторм'
    elif wnds < 28.4: wnds_str = 'Сильный шторм'
    elif wnds < 32.6: wnds_str = 'Жестокий шторм'
    elif wnds > 32.6: wnds_str = 'Ураган'
    emb.add_field(
        name= 'Степень ветра',
        value= wnds_str
    )
    emb.add_field(
        name= 'Скорость ветра',
        value= str(wnds) + ' м/с'
    )
    emb.set_image(url= w.get_weather_icon_url())
    await ctx.send(embed=emb)
@Bot.command()
async def wiki(ctx, *, text):
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(text)
    summ = wikipedia.summary(text)
    emb = discord.Embed(
        title= new_page.title,
        description= summ
    )
    emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

    await ctx.send(embed=emb)    
@Bot.command() # Попытки 5
async def numbers(ctx):
    await ctx.message.delete()
    num = random.randint(1, 20)
    print(num)
    attems = 1
    msg = await ctx.send('Подождите...')
    while attems < 6:
        emb = discord.Embed(
            title = f'Попытка №{attems}',
            description= 'Угадайте число от 1 до 20'
        )
        await msg.edit(content= None, embed=emb)
        
        try:
            msg_o = await  Bot.wait_for('message', timeout= 30.0, check= lambda msg_o: msg_o.author == ctx.author)
        except asyncio.TimeoutError:
            await msg.edit(content= 'Время вышло!', embed=None)
            break
        else:
            if num == int(msg_o.content):
                emb1 = discord.Embed(
                    title= 'Вы победили!',
                    description= 'Вы угадали число!'
                )
                await msg_o.delete()
                await msg.edit(content= None, embed=emb1)
                break
            else:
                attems_h = 5 - attems
                attems = attems + 1

                if attems == 6:
                    emb2 = discord.Embed(
                        title= 'Вы проиграли!',
                        description= f'Загаданое число было : {num}'
                    )
                    await msg_o.delete()
                    await msg.edit(embed=emb2)
                    break

                emb2 = discord.Embed(
                    title= 'Неудачная попытка!',
                    description= f'Вы не угадали число у вас осталось {attems_h} попыток'
                )
                await msg.edit(content= None, embed=emb2)
                await msg_o.delete() 
                await asyncio.sleep(5)
OPERATIONS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}
@Bot.command()
async def calc(ctx, a, operator, b):
    await ctx.send("Так кто не умеет считать я сделал за него и он получил:" + str(OPERATIONS[operator](int(a), int(b))))
@Bot.command(brief= '- makes the porridge from ur txt.')
async def rantxt(ctx, *, args):
    await ctx.send(f"{''.join(random.sample(args,len(args)))}")
@Bot.command()
async def webhook(ctx, *, text):
    w = await ctx.channel.create_webhook(name=ctx.author.name)
    await w.send(text, avatar_url=ctx.author.avatar_url)
@Bot.command()
async def youtube(ctx, *, question):  # пояндексить
    # сам сайт
    url = 'https://www.youtube.com/results?search_query=' + str(question).replace(' ', '+')
    await ctx.send(f'Так как кое кто не умеет ютубить , я сделал это за него.\n{url}')
@Bot.command()
async def serverinfo(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: Онлайн: **{online}**\n\n"
        f":black_circle: Оффлайн: **{offline}**\n\n"
        f":yellow_circle: Отошли: **{idle}**\n\n"
        f":red_circle: Не трогать: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)
@Bot.command()
async def inv(ctx, channel: discord.abc.GuildChannel):
    try:
        await ctx.message.delete()
    except Exception:
        pass

    log = Bot.get_channel(708331219460554812) 
    
    invitelink = await channel.create_invite(max_uses=100, max_age=21600, unique=True) #Настраиваем само приглашение - количество использований и длительность действия. Время в секундах

    emb = discord.Embed(
        title= 'Создано приглашение на сервер',
        color= discord.Color.orange()
    )
    emb.add_field(
        name= 'Приглашение создано участником:',
        value = ctx.author.mention
    )

    await ctx.author.send(f'Вы запросили ссылку-приглашение на сервер. Здорово! Теперь отправь eё другу:\n{invitelink}') #приглашение в ЛС пользователю
    await log.send(embed=emb)
@Bot.command()
async def зайцы(ctx, *, question):
    url = "https://zaycev.net/search.html?query_search=" + str(question).replace(" ", "+")
    await ctx.send(f"Музон захотел послушать ок лови\n{url}")
@Bot.command()
async def remind(ctx, time, arg, *, text):
    await ctx.send('Я напомню вам это!')

    if arg == "s":
        await asyncio.sleep(time) 

    elif arg == "m":
        await asyncio.sleep(time * 60)

    elif arg == "h":
        await asyncio.sleep(time * 60 * 60)

    elif arg == "d":
        await asyncio.sleep(time * 60 * 60 * 24)

    await ctx.author.send(text)

@Bot.command()
async def ball(ctx, *, arg):

    message = ['Нет','Да','Возможно','Опредленно нет', 'Попробуй ещё раз' ,'Даже не думай!' ,'Никогда!'  ] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'Кот кидает шар :pouting_cat: :right_facing_fist: :8ball:  \n и шар говорит ** {s}**', color=0x0c0c0c))
    return
@Bot.command()   
async def dice(ctx, od: int = None, ot: int = None):
    if od and ot:
        b = random.randint(od, ot)
        a = random.randint(od, ot)
        if b > a:
            await ctx.send(embed = discord.Embed(description = f'Ты проиграл! Боту выпало {b}, а тебе {a}. '))
        else:
            await ctx.send(embed=discord.Embed(description=f'Ты выиграл! Тебе выпало {a} а боту {b}'))
    else:
        await ctx.send(embed=discord.Embed(description='Укажите номера! (dice 1 12)')) 
@Bot.command()
async def giveaway(ctx, seconds: int, *, text):
    def time_end_form(seconds):
        h = seconds // 3600
        m = (seconds - h * 3600) // 60
        s = seconds % 60
        if h < 10:
            h = f"0{h}"
        if m < 10:
            m = f"0{m}"
        if s < 10:
            s = f"0{s}"
        time_reward = f"{h} : {m} : {s}"
        return time_reward

    author = ctx.message.author
    time_end = time_end_form(seconds)
    message = await ctx.send(embed=discord.Embed(
        description=f"**Разыгрывается : `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
        colour=0x75218f).set_footer(
        icon_url=ctx.message.author.avatar_url))
    await message.add_reaction("🎲")
    while seconds > -1:
        time_end = time_end_form(seconds)
        text_message = discord.Embed(
            description=f"**Разыгрывается: `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
            colour=0x75218f).set_footer(
            icon_url=ctx.message.author.avatar_url)
        await message.edit(embed=text_message)
        await asyncio.sleep(1)
        seconds -= 1
        if seconds < -1:
            break
    channel = message.channel
    message_id = message.id
    message = await channel.fetch_message(message_id)
    reactions = list(filter(lambda x: str(x.emoji) == "🎲", message.reactions))
    if len(reactions) == 0:
        users = []
    else:
        users = await reactions[0].users().flatten()
        users = list(filter(lambda x: not x.bot, users))

    if len(users) == 0:
        descr = '**В этом розыгрыше нет победителя!**'
    else:
        user_win = random.choice(users)
        descr = f'**Победитель розыгрыша: {user_win.mention}!\nНапишите организатору {author.mention}, чтобы получить награду.**'
    win = discord.Embed(
        description=descr,
        colour=0x75218f).set_footer(
        icon_url=ctx.message.author.avatar_url)
    await message.edit(embed=win)
@Bot.command()
async def gl( ctx, *, question ):

    url = 'https://google.gik-team.com/?q='
    emb = discord.Embed( title = question, description = 'Вот чего я должен все за тебя делать?',
                         colour = discord.Color.green(), url = url + str(question).replace(' ', '+') )
    
  
    

    await ctx.send( embed = emb )

@Bot.command()
@commands.is_owner()
async def load(ctx, extension):
    Bot.load_extension(f'Modules.{extension}')
    if not commands.NotOwner:
        await ctx.send(f"Ошибка доступа! Недостаточно прав.")
    else:
        await ctx.send(f"Модуль **{extension}** успешно загружен!")

@Bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    Bot.unload_extension(f'Modules.{extension}')
    if not commands.NotOwner:
        await ctx.send(f"Ошибка доступа! Недостаточно прав.")
    else:
        await ctx.send(f"Модуль **{extension}** успешно выгружен!")


@Bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    Bot.reload_extension(f'Modules.{extension}')
    if not commands.NotOwner:
        await ctx.send(f"Ошибка доступа! Недостаточно прав.")
    else:
        await ctx.send(f"Модуль **{extension}** успешно перезагружен!")


@Bot.command()
async def help( ctx  ):
	embed=discord.Embed(title="**Все команды бота**", color=0x56d625)
	embed.set_author(name="Твой жорик")
	embed.add_field(name="Общие команды  \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_thx Сказать спасибо или дать репу \n b_my_thx Моя репа или спасибо \n b_avatar(пинг)Покозать аву себя или пользователя \n b_servercount показывает где я есть \n b_ping посмотреть свой пинг \n b_ran_avatar случайная аниме ава \n b_hello привет боту \n b_profile(пинг) твой профиль или другого", inline=False)
	embed.add_field(name="Веселости  \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_pat [пинг] погладить \n b_slap [пинг] ударить\n b_kiss [пинг] поцеловать\n b_hug[пинг]обнять\n b_wiki[Текст]Википедия\n b_knb сыграть в КНБ! \n b_man Stonks \n b_wea [Город] Погода в городе \n b_numbers сыграть в угодайку n b_calc [число] [Оператор] [число] калькулятор\n b_remind [Время] [Текст] Напомнить \n  b_serverinfo Инфо о сервере ", inline=True)
	embed.add_field(name="Модераторское \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_kick[пинг][причина]кик человека\n b_ban[пинг](причина](время]бан человека\n b_unban[айди]разбан\n  \n b_clear[Кол-во сообшений] \n b_mute [человек] [прчина]вечный мут", inline=True)
	embed.add_field(name="Другое \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_ball[Вопрос] Кинуть шар \n b_dice[1 число] [2 число] сыграть в кости \n b_giveaway[Время в секундна][Вещь] Конкурс b_gl [Запрос] Я гуглю за вас( \n b_c0t Котики!!  \n b_vote Проголосовать за меня", inline=True)
	embed.add_field(name="Предложка \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_suggest [Идея]  предложить идею \n b_suggest_set  [канал] поставить канал идей \n b_suggest_off отключить", inline=True)
	embed.add_field(name="Жалобы \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_report [Жалобы]  жалобы на сервере или юзера \n b_report_set  [канал] поставить канал жалоб \n b_report_off  отключить", inline=True)
	embed.add_field(name="Спецальное \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="b_flag Сыграть в игру угодай флаг \n b_marry [Пинг] Поженится \n b_divorce Развестисть \n b_sap Сыграть в сапера", inline=True)
	embed.add_field(name="Приватные войсы \n `() Не обезательный аргумент` \n `[] Обезательный аргумент`", value="Для этого была создана отдельная мега красивая команлда b_privhelp", inline=True)
	await ctx.send( embed = embed )


@Bot.command()
@commands.cooldown(1, 60*60*24*2, commands.BucketType.member)
async def flag(ctx):
    with open('flags.json','r',encoding='utf8') as f: #открываем файл, который будет возле файла бота, и ставим кодировку utf-8 чтобы кириллица нормально отображалась и воспринималась
        flags = json.load(f) #получаем содержимое
        count = 1 #щас будет подсчёт раундов игры
        while count <= 10: #цикл игры, число 10 означает допустимое количество раундов, можете поменять
            otvet = random.choice(flags['Флаги']) #получаем рандомный флаг
            e = discord.Embed(title = f"Флаг {count}") #создаём эмбед
            e.set_image(url = otvet['url'])
            await ctx.send(embed = e)
            def check(m): #создаём проверку ответа
                return m.content == otvet['answer'] and ctx.channel == ctx.channel

            msg = await Bot.wait_for('message', check=check)
            em = discord.Embed(title = "Правильный ответ!") #пишет когда чел правильно ответил
            em.add_field(name = "Ответил:", value = f"{msg.author.mention}")
            em.add_field(name = "Правильный ответ:",value = f"{otvet['answer']}")
            await ctx.channel.send(embed = em)
            count = count + 1 #вступаем в следующий раунд
            await asyncio.sleep(1)
            if count == 11: #проверка
                e = discord.Embed(title = "Конец игры!", description = f"Ивент был проведён {ctx.author.mention}, и мы всем желаем удачи! Спасибо за участие!")
                await ctx.send(embed = e)





token = os.environ.get('BOT_TOKEN')

Bot.run(str(token))
