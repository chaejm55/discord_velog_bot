import discord
import random
from discord.ext import commands

token = '토큰 붙여넣기'
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


bot.run(token)