import disnake
from disnake.ext import commands
from Database import database

class BanRequestView(disnake.ui.View):
    def __init__(self, user: disnake.Member, emoji):
        super().__init__(timeout=60)
        self.message = None
        self.user = user
        self.emoji = emoji

    @disnake.ui.button(label="Да", style=disnake.ButtonStyle.danger)
    async def on_accept(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        await self.disable_buttons()
        await body.response.send_message(
                f"# {self.emoji} Система предупреждений\n"
                f"- Пользователь {self.user.mention} был ` заблокирован `",
                ephemeral=True
                )
        return await self.user.ban(
            reason="Пользователь получил слишком много предупреждений"
        )

    @disnake.ui.button(label="Нет", style=disnake.ButtonStyle.success)
    async def on_deny(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        await self.disable_buttons()
        return await body.response.send_message(
                f"# {self.emoji} Система предупреждений\n"
                f"- Вы решили не ` блокировать ` пользователя",
                ephemeral=True,
                )

    async def on_timeout(self):
        await self.disable_buttons()

    async def disable_buttons(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

class WarnFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = 1477235042475315240

    @commands.slash_command(description="Выдаёт предупреждение пользователю",
                            guild_ids=[1466509350100013226],
                            default_member_permissions=disnake.Permissions(administrator=True)
                            )
    async def warn(
            self,
            body: disnake.ApplicationCommandInteraction,
            пользователь: disnake.Member = commands.Param(
                description="Пользователь, который получит предупреждение"
                ),
            причина: str = commands.Param(
                description="Причина, по которой будет выдано предупреждение",
                min_length=5,
                max_length=100,
                default="Не указано"
                ),
            очистить: str = commands.Param(
                description="Очищает предупреждения, если требуется",
                choices=[
                    "Да",
                    "Нет"
                    ],
                default="Нет"
                )
            ):
        emoji = self.bot.get_emoji(self.emoji)
        async with database.db.execute("SELECT warns_value FROM users WHERE user_id = ?", (пользователь.id,)) as cursor:
            row = await cursor.fetchone()
        warns = row[0] if not None else 1
        if warns >= 3:
            view = BanRequestView(пользователь, emoji)
            await body.response.send_message(
                    f"# {emoji} Система предупреждений\n"
                    f"\n- Пользователь {пользователь.mention} имеет ` 3 / 3 ` предупреждений"
                    "\n> Вы хотите ` заблокировать ` его?",
                    ephemeral=True,
                    view=view
                    )
            view.message = await body.original_response()
            return
        if пользователь == self.bot:
            return await body.response.send_message(
                    f"# {emoji} Система предупреждений\n"
                    f"\n- Вы не можете выбрать ` бота `!",
                    ephemeral=True,
                    )
        if пользователь == body.author:
            return await body.response.send_message(
                    f"# {emoji} Система предупреждений\n"
                    f"\n- Вы не можете выбрать ` самого себя `!",
                    ephemeral=True,
                    )

        if self.is_clean(очистить):
            await database.db.execute(
                    """
                    UPDATE users SET warns_value = 0 WHERE user_id = ?
                    """,
                    (пользователь.id,)
                    )

            await database.db.commit()
            return await body.response.send_message(
                    f"# {emoji} Система предупреждений\n"
                    f"Предупреждения {пользователь.mention} были ` очищены `"
                    )
        await database.db.execute(
            """
            INSERT INTO users (user_id, warns_value)
            VALUES (?, 1)
            ON CONFLICT(user_id) DO UPDATE SET warns_value = warns_value + 1
            """,
            (пользователь.id,)
        )
        await database.db.commit()

        await body.response.send_message(
                f"# {emoji} Система предупреждений\n"
                f"\n- Администратор {body.author.mention} ` выдал ` предупреждение {пользователь.mention}"
                f"\n> Пользователь имеет ` {warns} / 3 ` предупреждений"
                f"\n> Причина: {причина}"
                )

    def is_clean(self, value: str) -> bool:
        return value == "Да"

def setup(bot):
    bot.add_cog(WarnFunction(bot))
