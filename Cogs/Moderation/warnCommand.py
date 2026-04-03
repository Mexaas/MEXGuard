import disnake
from disnake.ext import commands
from Database import database

class BanRequestView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.message = None

    @disnake.ui.button(label="пошёл нахуй")
    async def on_accept(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        return await body.response.send_message(
                f"Ну и пошёл он нахуй",
                ephemeral=True
                )
    @disnake.ui.button(label="я подумаю")
    async def on_deny(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        return await body.response.send_message(
                f"Ну ладно, пусть поживёт пока",
                ephemeral=True
                )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

class WarnFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        if self.is_clean(очистить):
            await database.db.execute(
                    """
                    UPDATE users SET warns_value = 0 WHERE user_id = ?
                    """,
                    (пользователь.id,)
                    )
            await database.db.commit()
            return await body.response.send_message(
                    f"Варны {пользователь.mention} были очищены",
                    ephemeral=True
                    )
        await database.db.execute(
            """
            INSERT INTO users (user_id, warns_value) 
            VALUES (?, 0) 
            ON CONFLICT(user_id) DO UPDATE SET warns_value = warns_value + 1
            """,
            (пользователь.id,)
        )
        await database.db.commit()

        async with database.db.execute("SELECT warns_value FROM users WHERE user_id = ?", (пользователь.id,)) as cursor:
            row = await cursor.fetchone()
        warns = row[0] if not None else 1

        if warns >= 3:
            view = BanRequestView()
            await body.response.send_message(
                    f"{пользователь.mention} уже имеет 3 варна"
                    "\nХотите ли вы ` заблокировать ` его?",
                    ephemeral=True,
                    view=view
                    )
            view.message = await body.original_response()
            return
        await body.response.send_message(
                f"Выдан варн {пользователь.mention}"
                f"\nПользователь имеет {warns} предупреждений",
                ephemeral=True
                )

    def is_clean(self, value: str) -> bool:
        return value == "Да"

def setup(bot):
    bot.add_cog(WarnFunction(bot))
