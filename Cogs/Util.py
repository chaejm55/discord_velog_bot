from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import openpyxl
import discord


class Util(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['코로나'])  # !코로나 입력 시에도 실행 가능
    async def crawl(self, ctx):
        url = "http://ncov.mohw.go.kr/"
        response = requests.get(url)
        response_code = int(response.status_code)  # 응답 코드 받기

        if response_code == 200:  # 정상 작동(코드 200 반환) 시
            soup = BeautifulSoup(response.content, 'lxml')
        else:  # 오류 발생
            return await ctx.send("웹 페이지 오류입니다.")

        # element 찾기

        # soup.find ()로 <div class="liveNum_today_new"> 에서 확진자 수 데이터가 들어 있는 <span class="data"> 리스트 가져오기
        today = soup.find("div", {"class": "liveNum_today_new"}).findAll("span", {"class": "data"})
        today_domestic = today[0].text  # 리스트 첫 번째 요소 (국내발생), int() 사용 대신 string으로 바로 넣음
        today_overseas = today[1].text  # 리스트 두 번째 요소 (해외유입), int() 사용 대신 string으로 바로 넣음
        today_total = format((int(today_domestic.replace(',', '')) + int(today_overseas.replace(',', ''))), ',')  # 일일 총 확진자 수를 따로 계산
        accumulate_confirmed = soup.find("div", {"class": "liveNum"}).find("span", {"class": "num"}).text[
                               4:]  # 앞에 (누적) 글자 자르기
        embed = discord.Embed(title="국내 코로나 확진자 수 현황", description="http://ncov.mohw.go.kr/ 의 정보를 가져옵니다.",
                              color=0x005666)
        embed.add_field(name="일일 확진자",
                        value=f"총: {today_total}명, 국내: {today_domestic}명, 해외유입: {today_overseas}명",
                        inline=False)
        embed.add_field(name="누적 확진자", value=f"{accumulate_confirmed}명", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="엑셀쓰기")
    async def write_excel(self, ctx, write_str: str):
        filename = "discord_bot.xlsx"
        book = openpyxl.load_workbook(filename)
        ws = book["discord_bot"]
        ws.append([str(ctx.author), write_str])
        book.save(filename)
        await ctx.send("엑셀 입력 완료!")

    @commands.command(name="엑셀읽기")
    async def read_excel(self, ctx):
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


def setup(bot):
    bot.add_cog(Util(bot))