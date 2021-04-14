import asyncio

import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup
from discord.ext.commands import MissingRequiredArgument, BadArgument
import requests
import openpyxl

load_dotenv()

token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')  # 봇의 접두사 설정


@bot.event
async def on_ready():  # 봇 준비 시 1회 동작하는 부분
    # 봇 이름 하단에 나오는 상태 메시지 설정
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("반갑습니다 :D"))
    print("Bot is ready")


@bot.event
async def on_raw_reaction_add(payload):
    banned_emoji = "👎"
    author = payload.user_id
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.emoji.name == banned_emoji and author != bot.user.id:
        await message.clear_reaction(banned_emoji)


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


def make_dir(directory_name):
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    except OSError:
        print('Error: makedirs()')


def add_result(directory_name, user_name, result):
    file_path = directory_name + '/' + user_name + '.txt'
    if os.path.exists(file_path):
        with open(file_path, 'a', encoding='UTF-8') as f:
            f.write(result)
    else:
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(result)


@bot.command()
async def game(ctx, user: str):
    rps_table = ['가위', '바위', '보']
    bot = random.choice(rps_table)
    result = rps_table.index(user) - rps_table.index(bot)
    if result == 0:
        result_text = f'{user} vs {bot} 비김'
        await ctx.send(f'{user} vs {bot}  비겼습니다.')
    elif result == 1 or result == -2:
        result_text = f'{user} vs {bot} 승리!'
        await ctx.send(f'{user} vs {bot}  유저가 이겼습니다.')
    else:
        result_text = f'{user} vs {bot} 패배...'
        await ctx.send(f'{user} vs {bot}  봇이 이겼습니다.')

    directory_name = "game_result"
    make_dir(directory_name)
    add_result(directory_name, str(ctx.author), result_text + '\n')


@game.error  # @<명령어>.error의 형태로 된 데코레이터를 사용한다.
async def game_error(ctx, error):  # 파라미터에 ctx, error를 필수로 한다.
    if isinstance(error, MissingRequiredArgument):  # isinstance로 에러에 따라 시킬 작업을 결정한다.
        await ctx.send("가위/바위/보 중 낼 것을 입력해주세요.")


@bot.command(name="전적")
async def game_board(ctx):
    user_name = str(ctx.author)
    file_path = "game_result/" + user_name + ".txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="UTF-8") as f:
            result = f.read()
        await ctx.send(f'{ctx.author}님의 가위바위보 게임 전적입니다.\n==============================\n' + result)
    else:
        await ctx.send(f'{ctx.author}님의 가위바위보 전적이 존재하지 않습니다.')


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


@bot.command(aliases=['해제'])
async def unban_user(ctx, nickname: str):
    ban_entry = await ctx.guild.bans()
    for users in ban_entry:
        if nickname == users.user.name:
            forgive_user = users.user
            await ctx.guild.unban(forgive_user)
            return await ctx.send(f"{nickname} 님이 차단 해제되었습니다.")
    return await ctx.send(f"{nickname} 님은 차단 목록에 없습니다.")


@bot.command(aliases=['역할부여'])
async def role_user(ctx, nickname: discord.Member, role_name):
    roles = ctx.guild.roles
    for role in roles:
        if role_name == role.name:
            await nickname.add_roles(role)
            return await ctx.send(f"{nickname} 님에게 {role_name} 역할이 부여 되었습니다.")
    return await ctx.send(f"{role_name} 역할이 존재하지 않습니다.")


@bot.command(aliases=['삭제'])
async def delete_msg(ctx):
    msg = await ctx.send("3초 뒤에 삭제 됩니다!")
    await msg.delete(delay=3)


@bot.command(aliases=['수정'])
async def edit_msg(ctx):
    msg = await ctx.send("곧 수정 됩니다!")
    await msg.edit(content="수정 되었습니다!")


@bot.command(name="따봉")
async def reaction(ctx):
    await ctx.message.add_reaction('👍')


@bot.command(name="기다리기")
async def wait(ctx):
    timeout = 5
    send_message = await ctx.send(f'{timeout}초간 기다립니다!')

    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.send(f'시간초과 입니다...({timeout}초)')
    else:
        await ctx.send(f'{msg.content}메시지를 {timeout}초 안에 입력하셨습니다!')


@bot.command(name="엑셀쓰기")
async def write_excel(ctx, write_str: str):
    filename = "discord_bot.xlsx"
    book = openpyxl.load_workbook(filename)
    ws = book["discord_bot"]
    ws.append([str(ctx.author), write_str])
    book.save(filename)
    await ctx.send("엑셀 입력 완료!")


@bot.command(name="엑셀읽기")
async def read_excel(ctx):
    filename = "discord_bot.xlsx"
    book = openpyxl.load_workbook(filename)
    ws = book["discord_bot"]
    result = []
    for row in ws.rows:
        if row[0].value == str(ctx.author):
            result.append(row[1].value)
    book.close()
    if result:
        await ctx.send(f'{ctx.author}님이 엑셀 파일에 입력한 내용들입니다.')
        await ctx.send('\n'.join(result))
    else:
        await ctx.send(f'{ctx.author}님이 엑셀 파일에 입력한 내용이 없습니다.')


bot.run(token)