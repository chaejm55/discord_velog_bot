import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')  # 봇의 접두사 설정

extensions = ['Game', 'User', 'Msg', 'Util']

for ext in extensions:
    bot.load_extension(ext)


@bot.event
async def on_ready():  # 봇 준비 시 1회 동작하는 부분
    # 봇 이름 하단에 나오는 상태 메시지 설정
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("반갑습니다 :D"))
    print("Bot is ready")


@bot.command()  # 봇 명령어
async def hello(ctx):  # !hello라고 사용자가 입력하면
    await ctx.send("Hello world")  # 봇이 Hello world!라고 대답함


@bot.command(usage='test usage', description='test description', help='test help')
async def test(ctx):
    await ctx.send("test")


bot.run(token)
