from discord.ext import commands
import discord


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['추방'])
    async def kick_user(self, ctx, nickname: discord.Member):
        await nickname.kick()
        await ctx.send(f"{nickname} 님이 추방되었습니다.")

    @commands.command(aliases=['차단'])
    async def ban_user(self, ctx, nickname: discord.Member):
        await nickname.ban()
        await ctx.send(f"{nickname} 님이 차단되었습니다.")

    @commands.command(aliases=['해제'])
    async def unban_user(self, ctx, nickname: str):
        ban_entry = await ctx.guild.bans()
        for users in ban_entry:
            if nickname == users.user.name:
                forgive_user = users.user
                await ctx.guild.unban(forgive_user)
                return await ctx.send(f"{nickname} 님이 차단 해제되었습니다.")
        return await ctx.send(f"{nickname} 님은 차단 목록에 없습니다.")

    @commands.command(aliases=['역할부여'])
    async def role_user(self, ctx, nickname: discord.Member, role_name):
        roles = ctx.guild.roles
        for role in roles:
            if role_name == role.name:
                await nickname.add_roles(role)
                return await ctx.send(f"{nickname} 님에게 {role_name} 역할이 부여 되었습니다.")
        return await ctx.send(f"{role_name} 역할이 존재하지 않습니다.")


def setup(bot):
    bot.add_cog(User(bot))
