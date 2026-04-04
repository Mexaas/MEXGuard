import disnake
from disnake.ext import commands
import asyncio
from Database import database

class UserFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = 1477235042475315240

    @commands.slash_command(description="Анализирует пользователя",
                            guild_ids=[1466509350100013226],
                            default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def user(self, body: disnake.ApplicationCommandInteraction, пользователь: disnake.Member = commands.Param(
        description="Пользователь, которого нужно проанализировать"
    )):
        if пользователь == self.bot or пользователь == body.author:
            return await body.response.send_message(
                "# :x: Ошибка\n"
                "- Укажите корректного пользователя",
                ephemeral=True
            )
        emoji = self.bot.get_emoji(self.emoji)
        async with database.db.execute(
            """
            SELECT warns_value FROM users WHERE user_id = ?
            """,
            (пользователь.id,)
        ) as cursor:
            row = await cursor.fetchone()
            warns_value = row[0] if row else 0
        await body.response.send_message(
            f"Анализирую пользователя {пользователь.mention}...",
            ephemeral=True
        )
        await asyncio.sleep(2)
        await body.edit_original_response(
            f"# {emoji} Информация об {пользователь.mention}"
            f"\n- Предупреждения: ` {warns_value} / 3 `"
            f"\n> Находится в войсе: ` {"Да" if пользователь.voice else "Нет"} `"
            f"\n> Зашёл на сервер: ` {пользователь.joined_at[:21]} `"
            f"\n> Высшая роль: {пользователь.top_role.mention}"
        )

def setup(bot):
    bot.add_cog(UserFunction(bot))
