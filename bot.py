import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(verbose=True)

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')  # 봇의 접두사 설정

# cogs 폴더의 절대 경로 얻기
# Pycharm에서 바로 상대 경로를 사용하면 오류가 발생하기 때문에 따로 절대경로를 얻어야한다.
cogs_path = 'Cogs'
abs_cogs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), cogs_path)

# cogs 폴더에 존재하는 cogs(.py파일) 로드
for ext in os.listdir(abs_cogs_path):
    if ext.endswith(".py"):
        bot.load_extension(f"Cogs.{ext.split('.')[0]}")  # .py 부분을 떼고 cog의 이름만 추출


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
