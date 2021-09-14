from discord.ext import commands
from discord.ext.commands import BadArgument
import discord
import asyncio


class Msg(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_raw_reaction_add')
    async def on_raw_reaction_add(self, payload):
        banned_emoji = "👎"
        author = payload.user_id
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if payload.emoji.name == banned_emoji and author != self.bot.user.id:
            await message.clear_reaction(banned_emoji)

    @commands.command(name="숫자")
    async def num_echo(self, ctx, user: int):
        await ctx.send(f"입력한 숫자는 {user}입니다.")

    @num_echo.error
    async def num_echo_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("정수를 입력 해주세요")

    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="Embed title", description="Embed description", color=0x36ccf2)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")
        embed.set_image(url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")
        embed.add_field(name="field_name1", value="field value1", inline=False)
        embed.add_field(name="field_name2", value="field value2", inline=False)
        embed.add_field(name="field_name3", value="field value3", inline=False)
        embed.add_field(name="field_name4", value="field value4", inline=False)
        embed.set_footer(text="footer_text",
                         icon_url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")
        embed.set_author(name="author_name", url="https://velog.io/@chaejm55",
                         icon_url="https://cdn.discordapp.com/attachments/721307978455580742/762760779409129513/img.png")

        await ctx.send(embed=embed)

    @commands.command(aliases=['삭제'])
    async def delete_msg(self, ctx):
        msg = await ctx.send("3초 뒤에 삭제 됩니다!")
        await msg.delete(delay=3)

    @commands.command(aliases=['수정'])
    async def edit_msg(self, ctx):
        msg = await ctx.send("곧 수정 됩니다!")
        await msg.edit(content="수정 되었습니다!")

    @commands.command(name="따봉")
    async def reaction(self, ctx):
        await ctx.message.add_reaction('👍')

    @commands.command(name="기다리기")
    async def wait(self, ctx):
        timeout = 5
        send_message = await ctx.send(f'{timeout}초간 기다립니다!')

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            await ctx.send(f'시간초과 입니다...({timeout}초)')
        else:
            await ctx.send(f'{msg.content}메시지를 {timeout}초 안에 입력하셨습니다!')

            
def setup(bot):
    bot.add_cog(Msg(bot))
