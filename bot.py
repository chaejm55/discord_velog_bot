import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup
from discord.ext.commands import MissingRequiredArgument, BadArgument
import requests

load_dotenv()

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')  # 봇의 접두사 설정


@bot.event
async def on_ready():  # 봇 준비 시 1회 동작하는 부분
    # 봇 이름 하단에 나오는 상태 메시지 설정
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("반갑습니다 :D"))
    print("Bot is ready")


@bot.command()  # 봇 명령어
async def hello(ctx):  # !hello라고 사용자가 입력하면
    await ctx.send("Hello world")  # 봇이 Hello world!라고 대답함


@bot.command()
async def dice(ctx):
    randnum = random.randint(1, 6)
    await ctx.send(f'주사위 결과는 {randnum} 입니다.')


@bot.command()
async def mining(ctx):
    minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
    weights = [1, 3, 6, 15, 25, 50]
    results = random.choices(minerals, weights=weights, k=5)
    await ctx.send(', '.join(results) + ' 광물들을 획득하였습니다.')


@bot.command()
async def game(ctx, user: str):
    rps_table = ['가위', '바위', '보']
    bot = random.choice(rps_table)
    result = rps_table.index(user) - rps_table.index(bot)
    if result == 0:
        await ctx.send(f'{user} vs {bot}  비겼습니다.')
    elif result == 1 or result == -2:
        await ctx.send(f'{user} vs {bot}  유저가 이겼습니다.')
    else:
        await ctx.send(f'{user} vs {bot}  봇이 이겼습니다.')


@game.error  # @<명령어>.error의 형태로 된 데코레이터를 사용한다.
async def game_error(ctx, error):  # 파라미터에 ctx, error를 필수로 한다.
    if isinstance(error, MissingRequiredArgument):  # isinstance로 에러에 따라 시킬 작업을 결정한다.
        await ctx.send("가위/바위/보 중 낼 것을 입력해주세요.")
        

@bot.command(name="숫자")
async def num_echo(ctx, user: int):
    await ctx.send(f"입력한 숫자는 {user}입니다.")


@num_echo.error
async def num_echo_error(ctx, error):
    if isinstance(error, BadArgument):
        await ctx.send("정수를 입력 해주세요")


@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Embed title", description="Embed description", color=0x36ccf2)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")
    embed.add_field(name="field_name1", value="field value1", inline=False)
    embed.add_field(name="field_name2", value="field value2", inline=False)
    embed.add_field(name="field_name3", value="field value3", inline=False)
    embed.add_field(name="field_name4", value="field value4", inline=False)
    embed.set_footer(text="footer_text", icon_url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")
    embed.set_author(name="author_name", url="https://velog.io/@chaejm55", icon_url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")

    await ctx.send(embed=embed)


@bot.command(usage='test usage', description='test description', help='test help')
async def test(ctx):
    await ctx.send("test")


@bot.command(aliases=['코로나'])  # !코로나 입력 시에도 실행 가능
async def crawl(ctx):
    url = "http://ncov.mohw.go.kr/"
    response = requests.get(url)
    response_code = int(response.status_code)  # 응답 코드 받기


    if response_code == 200:  # 정상 작동(코드 200 반환) 시
        soup = BeautifulSoup(response.content, 'lxml')
    else:  # 오류 발생
        await ctx.send("웹 페이지 오류입니다.")

    # element 찾기

    # soup.find ()로 <div class="liveNum_today_new"> 에서 확진자 수 데이터가 들어 있는 <span class="data"> 리스트 가져오기
    today = soup.find("div", {"class": "liveNum_today_new"}).findAll("span", {"class": "data"})
    today_domestic = int(today[0].text)  # 리스트 첫 번째 요소 (국내발생)
    # today_domestic = int(soup.select_one("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li:nth-child(1) > span.data").text)
    today_overseas = int(today[1].text) # 리스트 두 번째 요소 (해외유입)
    accumulate_confirmed = soup.find("div", {"class": "liveNum"}).find("span", {"class": "num"}).text[4:]  # 앞에 (누적) 글자 자르기
    embed = discord.Embed(title="국내 코로나 확진자 수 현황", description="http://ncov.mohw.go.kr/ 의 정보를 가져옵니다.", color=0x005666)
    embed.add_field(name="일일 확진자",
                value=f"총: {today_domestic + today_overseas}, 국내: {today_domestic}, 해외유입: {today_overseas}",
                inline=False)
    embed.add_field(name="누적 확진자", value=f"{accumulate_confirmed}명", inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['추방'])
async def kick_user(ctx, nickname: discord.Member):
    await nickname.kick()
    await ctx.send(f"{nickname} 님이 추방되었습니다.")


@bot.command(aliases=['차단'])
async def ban_user(ctx, nickname: discord.Member):
    await nickname.ban()
    await ctx.send(f"{nickname} 님이 차단되었습니다.")

bot.run(token)