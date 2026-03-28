import disnake
from pathlib import Path
from datetime import timedelta
from disnake.ext import commands

class SlapCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [1477235374127452160]
    #     self.image_type = {
    #         "slap_command": "Content/SlapCommand_Image.png"
    #     }
    # def get_image(self, value: str) -> disnake.File:
    #     return disnake.File(self.image_type[value], Path(self.image_type[value]).name)

    allowed_answers = ["Да", "Нет"]
    @commands.slash_command(description="Отправить пользователя подумать о своем поведении",
     guild_ids=[1466509350100013226],
     default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def slap(self, body: disnake.ApplicationCommandInteraction,
        снять_наказание: str = commands.Param(
            description="Отметьте, чтобы снять наказание пользователю",
            choices=allowed_answers,
        ),
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
            return await body.response.send_message("# :x: Ошибка\n- Укажите ` правильные ` аргументы",
                ephemeral=True, delete_after=10
            )
        match снять_наказание.lower():
            case "да":
                await body.response.send_message(
                    f"# {self.bot.get_emoji(self.emojis[0])} Система намордников"
                    f"\n- {body.author.mention} ` снял ` намордник пользователю {пользователь.mention}"
                    f"\n> Причина: {причина}",
                    delete_after=240
                )
                return await пользователь.timeout(reason=причина, duration=None)
            case _:
                await пользователь.timeout(
                    reason=причина,
                    duration=timedelta(
                        minutes=время
                    )
                )
                return await body.response.send_message(
                    f"# {self.bot.get_emoji(self.emojis[0])} Система намордников"
                    f"\n- {body.author.mention} ` надел ` намордник пользователю {пользователь.mention} на ` {время} ` мин."
                    "\nЕму стоит ` подумать ` над своим поведением!"
                    f"\n> Причина: {причина}",
                    delete_after=240
                )

def setup(bot):
    bot.add_cog(SlapCommand(bot))
