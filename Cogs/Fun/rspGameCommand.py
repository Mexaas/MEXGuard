import disnake
from disnake.ext import commands

class RockPaperScissorsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Отправить дуэль на камень, ножницы, бумага", guild_ids=[1466509350100013226])
    async def rock(self,
        body: disnake.ApplicationCommandInteraction,
        пользователь: disnake.Member = commands.Param(description="Пользователь, который получит предложение")
    ):
        await body.response.send_message(f"{пользователь.mention}")

def setup(bot):
    bot.add_cog(RockPaperScissorsCommand(bot))
