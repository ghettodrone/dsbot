import discord, asyncio, time
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from itertools import cycle
import random 
import ctypes
import json
import os
import re
from datetime import datetime
from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl







Bot = commands.Bot(command_prefix= '?')

Bot.remove_command('help')

report_file = 660923073712619530 # int. Вставить id канала репортов, обязательно

@Bot.command()
async def clear(ctx, amount= 99):
    await ctx.channel.purge(limit=amount)

@Bot.command(pass_context= True)
async def help(ctx):
    emb = discord.Embed(title= "Info about commands", colour= 0xb0fe0a)
    emb.set_author(name= Bot.user.name , icon_url= 'https://cdn.discordapp.com/avatars/610551362161344522/a069df5f08d1cbe6b9c01e6505543c69.webp?size=1024')
    emb.add_field(name= "**.help**", value= "__Показывает команды бота__")
    emb.add_field(name= "**.info**", value= "__Дает информацию о пользователе__")
    emb.add_field(name= "**.avatar**", value= "__Находит аватарку в интернете__")
    emb.add_field(name= "**.kick**", value= "__Кикает участника с сервера__")
    emb.add_field(name= "**.hello**", value= "__Отправляет коронное приветствие__")
    emb.add_field(name= "**.ping**", value= "__Показывает скорость ответа бота__")
    emb.add_field(name= "**.botinfo**", value= "__Дает полную информацию о боте__")
    emb.add_field(name= "**.ban**", value= "__Банит игрока на сервере__")
    await ctx.send(embed= emb)
    await ctx.message.delete()


@Bot.event
async def on_raw_reaction_add(payload): 
        message_id = payload.message_id
        if message_id == 667053507626532878:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, Bot.guilds)

            if payload.emoji.name == 'python':
                role = discord.utils.get(guild.roles, name= 'python')
            elif payload.emoji.name == 'cpp':
                role = discord.utils.get(guild.roles, name= 'c++')
            elif payload.emoji.name == 'csharp':
                role = discord.utils.get(guild.roles, name= 'c#')
            elif payload.emoji.name == 'javascript':
                role = discord.utils.get(guild.roles, name= 'javascript')
            elif payload.emoji.name == 'dota':
                role = discord.utils.get(guild.roles, name= 'dota')
            elif payload.emoji.name == 'pubg':
                role = discord.utils.get(guild.roles, name= 'pubg')
            elif payload.emoji.name == 'csgo':
                role = discord.utils.get(guild.roles, name= 'csgo')
            elif payload.emoji.name == 'fortnite':
                role = discord.utils.get(guild.roles, name= 'fortnite')
            elif payload.emoji.name == 'boy':
                role = discord.utils.get(guild.roles, name= 'boy')
            elif payload.emoji.name == 'girl':
                role = discord.utils.get(guild.roles, name= 'girl')
            elif payload.emoji.name == 'trap':
                role = discord.utils.get(guild.roles, name= 'trap')
            else:
                pass


            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("done")
                else:
                    permission_error = str('Sorry ' + ctx.message.author + ' you do not have permissions to do that!')
                    print(permission_error)

@Bot.command()
async def join(ctx):
    
	channel = ctx.message.author.voice.channel
	voice = get(Bot.voice_clients, guild= ctx.guild)


	if voice and voice.is_connected(channel):
    		await voice.move_to(channel)
	else:
    		voice = await channel.connect()

	await voice.disconnect()

	if voice and voice.is_connected():
    		await voice.move_to(channel)
	else:
			voice = await channel.connect()
            
  





@Bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@Bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(Bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")

@Bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(Bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@Bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(Bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")



ydl_opts1 = {
    'format' : 'bestaudio/beat',
    'postprocessors' : [{
        'key' : 'FFmpegPCMAudio',
        'preferredcodec' : 'mp3',
        'preferredquality': '192',
    }]
}

	

@Bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return



    voice = get(Bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")










@Bot.command()
async def report(ctx, member: discord.Member, reason= None):
	channel = Bot.get_channel(report_file)
	author = ctx.author
	if ctx.message.guild is None:
		pass
	else:
		await ctx.message.delete()

		try:
			log_report_embed = discord.Embed(title= "⚠ Report",  description= f"**Пользователь:**\n<@{member.id}>  `ID: {member.id}`\n**Канал:**\n<#{ctx.message.channel.id}>\n**Причина**\n{reason}", colour= 0xFF1493)
			log_report_embed.set_author(name= f'{ctx.message.author}  ({ctx.message.author.id})', icon_url=ctx.message.author.avatar_url)
			await channel.send(embed= log_report_embed)

			report_embed=discord.Embed(description= f'Ваша жалоба на <@{member.id}> принята.', colour= 0xFF1493)
			report_embed.set_footer(text='Большая просьба воздержаться от спама, 1 жалобы на пользователя вполне достаточно.')
			await author.send(embed= report_embed)
		except:
			try:
				await author.send(embed= discord.Embed(description='⚠ Произошла ошибка. обратитесь к главному создателю!', colour= 0xFF1493)) 
			except:
				pass







logfile = 614922990374617118 # int. Вставить id канала логов, обязательно
botid = 610551362161344522 # int. Вставить id бота, обязательно

status = ['за KASQ','Порно', '?help']

@Bot.event
async def on_ready():
    print("Ботик на месте йоу")
    print("--------------------")
    print('Logged in as')
    print("--------------------")
    print(Bot.user.name)
    print("--------------------")
    print(Bot.user.id)
    print('--------------------')

    while True:
        for i in status:
            await Bot.change_presence(status= discord.Status.dnd, activity=discord.Activity(name= i, type=discord.ActivityType.watching))
            await asyncio.sleep(10)




@Bot.command()
@commands.has_any_role("Великий человек", "Свои Люди", "Специальный администратор", "кодер")
async def say(ctx, *, value=None):
    message = ctx.message
    if value != None:
        temp = value.split(" ", maxsplit=1)
        channel = message.channel
        if len(temp) > 1:
            channel = temp[0]
            channel = re.sub(r'[<@#&!>]+', '', channel)
            channel = Bot.get_channel(channel)
            if channel:
                value = temp[1]
            else:
                channel = message.channel
        try:
            await ctx.message.delete()
        except:
            pass
        text, em = await get_embed(value)
        await channel.send(content=text, embed=em)
        return
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        err =await ctx.send("Укажите значение!")
        await asyncio.sleep(6)
        try:
            await err.delete()
        except:
            pass

 
 




@Bot.event
async def get_embed(value):
    try:
        ret = json.loads(value)
        if ret and isinstance(ret, dict):
            em = discord.Embed(**ret)
            if "author" in ret.keys():
                em.set_author(
                    name=ret["author"].get("name"),
                    url=ret["author"].get("url", discord.Embed.Empty),
                    icon_url=ret["author"].get("icon_url", discord.Embed.Empty)
                )
            if "footer" in ret.keys():
                em.set_footer(
                    text=ret["footer"].get("text", discord.Embed.Empty),
                    icon_url=ret["footer"].get("icon_url", discord.Embed.Empty)
                )
            if "image" in ret.keys():
                em.set_image(
                    url=ret["image"]
                )
            if "thumbnail" in ret.keys():
                em.set_thumbnail(
                    url=ret["thumbnail"]
                    )
            if "fields" in ret.keys():
                for field in ret["fields"]:
                    try:
                        em.add_field(
                            name=field.get("name"),
                            value=field.get("value"),
                            inline=field.get("inline", False)
                        )
                    except:
                        pass
        if "text" in ret.keys():
            text = ret["text"]
        else:
            text = None
    except:
        text = value
        em = None
    return text, em
		





@Bot.command(pass_context= True)
@commands.has_permissions(ban_members= True)
async def ban(ctx, member: discord.Member, reason= None):
    await member.ban(reason=reason)
    await ctx.message.delete()
    emb = discord.Embed(title= "**Участник __{}__, был забанен.**".format(member.name.mention), colour= 0xb0fe0a)
    await ctx.send(embed= emb)

@Bot.command(pass_context= True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason= None):
    await member.kick()
    await ctx.message.delete()
    emb = discord.Embed(title= "**Участник __{}__, был кикнут.**".format(member.name), colour= 0x3600ff)
    await ctx.send(embed= emb)






@Bot.command()
async def avatar(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    await ctx.message.delete()
    embed = discord.Embed(title= f"Аватар пользователя {user}", colour= 0xb0fe0a, description= f'[Ссылка на изображение]({user.avatar_url})', color= 0xb0fe0a)
    embed.set_author(name= Bot.user.name , icon_url= 'https://cdn.discordapp.com/avatars/610551362161344522/a069df5f08d1cbe6b9c01e6505543c69.webp?size=1024')
    embed.set_image(url= user.avatar_url)
    await ctx.send(embed= embed)


@Bot.command(pass_context= True)
async def info(ctx, member: discord.Member):
    emb = discord.Embed(title= "``Информация о {}``".format(member.name), colour= 0x3600ff)
    emb.add_field(name= "**Имя**", value= member.name)
    emb.add_field(name= "**Когда присоединился**", value= str(member.joined_at)[:16])
    emb.add_field(name= "**ID**", value= member.id)
    emb.add_field(name= "**Roles**", value= member.top_role)
    emb.add_field(name= "**Game**", value= member.activities)
    emb.set_author(name= Bot.user.name, icon_url= 'https://cdn.discordapp.com/avatars/610551362161344522/c3186aab6fae251f92262fd9b958d51b.webp?size=1024')
    await ctx.send(embed= emb)
    await ctx.message.delete()


@Bot.command()
@commands.has_permissions(administrator= True)
async def mute(ctx, member: discord.Member = None, tm = "infinite", *, reason = "Не указанна"): # Мут игрока на определенное время, Пример - #mute @HaCsO#9577 10(в минутах) Оскорбления
	if not member: # Проверка, указан игрок которому будет выдан мут, или нет							
		await ctx.message.delete() # Удаления сообщения с командой
		ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал
	
	else: # Выводится при наличии игрока
		await ctx.message.delete() # Удаления сообщения с командой
		if tm == "infinite": # Проверка, если срок навечно, то выполняется этот блок
			membern = member.nick # Взятие ника игрока в переменную
			if member.nick == None: # Проверка наличия самого ника
				membern = member.name # изменение ника на имя аккаунта
			mute_cnt = f"Пользователь {membern} быз замучен на неопределенный срок админом {ctx.author.mention}\nпричина:\n{reason}!" # Переменная с текстом
			mute = discord.Embed(title= "Mute", description= mute_cnt, colour= 0x3600ff) # Создание таблицы
			role = discord.utils.get(ctx.message.guild.roles, name= 'Muted') # Поиск вышеуказанной роли для мута
			await member.add_roles(role) # Выдача этой роли указанному игроку
			await ctx.send(embed= mute) # Сообщение в чат о успешном муте
		else:
			membern = member.nick # Взятие ника игрока в переменную
			if member.nick == None: # Проверка наличия самого ника
				membern = member.name # изменение ника на имя аккаунта
			mute_cnt = f"Пользователь {membern} быз замучен на {tm} минут админом {ctx.author}\nпричина:\n{reason}!" # Переменная с текстом
			unmute_cnt = f"Пользователь {membern} быз раззамучен!" # Переменная с текстом
			role = discord.utils.get(ctx.message.guild.roles, name= 'Muted') # Поиск вышеуказанной роли для мута
			mute = discord.Embed(title= "Mute", description= mute_cnt, colour=  0x3600ff ) # Создание таблицы
			unmute = discord.Embed(title= "UnMute", description= unmute_cnt, colour= 0x3600ff ) # Создание таблицы
			t = (int(tm) * 60) # Изменение формата с секунд на минуты
			await member.add_roles(role) # Добавление роли замученного указанному игроку
			await ctx.send(embed= mute) # Отправка сообщения об этом
			await asyncio.sleep(t) # Задержка до разбана
			await member.remove_roles(role) # Снятие роли замученного
			await ctx.send(embed= unmute) # Отправка сообщения об этом






@Bot.command()
@commands.has_permissions(administrator= True)
async def unmute(ctx, member : discord.Member = None): # размут игрока, пример - #unmute @HaCsO#9577
	await ctx.message.delete() # Удаления сообщения с командой
	if not member: # Проверка, указан игрок которому будет выдан размут, или нет
		ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал
	else: # Выводится при наличии игрока
		membern = member.nick # Взятие ника игрока в переменную
		if member.nick == None: # Проверка наличия самого ника
			membern = member.name # изменение ника на имя аккаунта
		unmute_cnt = f"Пользователь {membern} быз размучен админом {ctx.author.mention}!" # Переменная с текстом
		unmute = discord.Embed(title= "UnMute", description= unmute_cnt, colour= 0x3600ff) # Создание таблицы
		role = discord.utils.get(ctx.message.guild.roles, name= 'Muted') # Поиск вышеуказанной роли для мута
		await member.remove_roles(role) # Снятие роли замученного
		await ctx.send(embed= unmute) # Отправка сообщения об этом




@Bot.command()
@commands.has_permissions(administrator= True)
async def warn(ctx, member : discord.Member = None, *, reason = None): # Разбанивает игрока, Пример - #unban @HaCsO#9577 Обман	
	await ctx.message.delete() # Удаления сообщения с командой
	if not member: # Проверка, указан игрок которому будет выдан варн, или нет
		await ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал
		
	else:
		role = discord.utils.get(ctx.message.guild.roles, name= 'Ban Global') # Поиск вышеуказанной роли бана

		unban_cnt = f"Администратор {ctx.author.mention} выдал варн <@{member.id}>\nпричина:\n{reason}" # Переменная с текстом
		unban = discord.Embed(title= "Warned", description= unban_cnt, color= 0x3600ff ) # Создание таблицы
		await member.add_roles(role) # Удаление роли забаненного у указанного игрока
		await ctx.send(embed= unban) # Отправка сообщения об этом




@Bot.command()
@commands.has_permissions(administrator= True)
async def unban(ctx, member : discord.Member = None, *, reason = None): # Разбанивает игрока, Пример - #unban @HaCsO#9577 Обман	
	await ctx.message.delete() # Удаления сообщения с командой
	if not member: # Проверка, указан игрок которому будет выдан варн, или нет
		await ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал
		
	else:
		role = discord.utils.get(ctx.message.guild.roles, name= 'Ban Global') # Поиск вышеуказанной роли бана

		unban_cnt = f"Администратор {ctx.author.mention} разбанил пользователя <@{member.id}>\nпричина:\n{reason}" # Переменная с текстом
		unban = discord.Embed(title= "UnWarned", description= unban_cnt, color= 0x3600ff ) # Создание таблицы
		await member.remove_roles(role) # Удаление роли забаненного у указанного игрока
		await ctx.send(embed= unban) # Отправка сообщения об этом








@Bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id =605056528323706891)
    channel = Bot.get_channel(635550925439762462)
    emb = discord.Embed(title= "Здарова!,** {} **".format(member.name), description= "Советую, заглянуть в канал {#правила}.\n Чтобы получить рольку, которая тебе по душе зайди в {#roles}. ", color= 0x3600ff)
    emb.set_author(name= "KASQ" , icon_url= 'https://cdn.discordapp.com/avatars/610551362161344522/c3186aab6fae251f92262fd9b958d51b.webp?size=1024')
    emb.set_image(url= 'https://cdn.discordapp.com/attachments/605056149925920778/662600096352829440/8003416_184013fb.gif')
    emb.set_footer(text= 'ID: {}'.format(member.id), icon_url= member.avatar_url)
    await channel.send(embed= emb) 
    await member.add_roles(role)















Bot.run('token')


