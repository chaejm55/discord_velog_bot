import random
import os
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument


async def make_dir(directory_name):
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    except OSError:
        print('Error: makedirs()')


async def add_result(directory_name, user_name, result):
    file_path = directory_name + '/' + user_name + '.txt'
    if os.path.exists(file_path):
        with open(file_path, 'a', encoding='UTF-8') as f:
            f.write(result)
    else:
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(result)


class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx):
        randnum = random.randint(1, 6)
        await ctx.send(f'주사위 결과는 {randnum} 입니다.')

    @commands.command()
    async def mining(self, ctx):
        minerals = ['다이아몬드', '루비', '에메랄드', '자수정', '철', '석탄']
        weights = [1, 3, 6, 15, 25, 50]
        results = random.choices(minerals, weights=weights, k=5)
        await ctx.send(', '.join(results) + ' 광물들을 획득하였습니다.')

    @commands.command()
    async def game(self, ctx, user: str):
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
    async def game_error(self, ctx, error):  # 파라미터에 ctx, error를 필수로 한다.
        if isinstance(error, MissingRequiredArgument):  # isinstance로 에러에 따라 시킬 작업을 결정한다.
            await ctx.send("가위/바위/보 중 낼 것을 입력해주세요.")

    @commands.command(name="전적")
    async def game_board(self, ctx):
        user_name = str(ctx.author)
        file_path = "game_result/" + user_name + ".txt"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="UTF-8") as f:
                result = f.read()
            await ctx.send(f'{ctx.author}님의 가위바위보 게임 전적입니다.\n==============================\n' + result)
        else:
            await ctx.send(f'{ctx.author}님의 가위바위보 전적이 존재하지 않습니다.')


def setup(bot):
    bot.add_cog(Game(bot))
