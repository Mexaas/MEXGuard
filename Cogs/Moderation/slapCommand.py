import disnake
from datetime import timedelta
from disnake.ext import commands

class SlapCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Отправить пользователя подумать о своем поведении",
     guild_ids=[1466509350100013226],
     default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def slap(self, body: disnake.ApplicationCommandInteraction,
        пользователь: disnake.Member = commands.Param(
            description="Пользователь, которого хотите наказать"
        ),
        причина: str = commands.Param(
            description="Причина наказания",
            default="Не указано",
            min_length=3,
            max_length=50
        ),
        время: int = commands.Param(description="Время таймаута в минутах", default=10, le=40320)
    ):
        if пользователь == body.author or self.bot.user == пользователь:
            return await body.response.send_message("# :x: Ошибка\n- Введите правильные параметры",
                ephemeral=True, delete_after=10
            )
        await пользователь.timeout(
            reason=причина,
            duration=timedelta(
                minutes=время
            )
        )

def setup(bot):
    bot.add_cog(SlapCommand(bot))
