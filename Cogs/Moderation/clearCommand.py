import disnake
import asyncio
from disnake.ext import commands

class ClearView(disnake.ui.View):
    def __init__(self, bot, emoji_id: int, author: disnake.Member, delete_bot_messages: str, mentioned_user: disnake.Member):
        super().__init__(timeout=60)
        self.emoji = bot.get_emoji(emoji_id)
        self.message = None
        self.clear_value = None
        self.author = author
        self.bot = bot
        self.delete_bot_messages = delete_bot_messages
        self.mentioned_user = mentioned_user

    @disnake.ui.button(label="Подтвердить", style=disnake.ButtonStyle.success)
    async def accept_callback(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.author: return await body.response.send_message(
            "# :x: Ошибка\n"
            "- Вы не можете отвечать за ` другого ` пользователя!",
            ephemeral=True,
            delete_after=10
        )
        try:
            def check(message):
                delete_bots = self.is_bot_messages_delete(); delete_user = self.is_user_messages_delete()

                if not delete_bots and not delete_user:
                    return not message.author.bot
                matches_bot = delete_bots and message.author.bot
                matches_user = delete_user and message.author == self.mentioned_user

                return matches_bot or matches_user

            await body.response.edit_message(
                f"# {self.emoji} Очистка"
                f"\n- Сжираю ` {self.clear_value} ` сообщений...",
                view=None
            )
            await body.channel.purge(
                limit=self.clear_value,
                check=check
            )
            await asyncio.sleep(1)
            return await body.edit_original_response(
                f"# {self.emoji} Очистка"
                f"\n- Съел ` {self.clear_value} ` сообщений. Было очень вкусно",
                view=None,
                delete_after=20
            )
        except disnake.NotFound:
            return

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.danger)
    async def deny_callback(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.author: return await body.response.send_message(
            "# :x: Ошибка\n"
            "- Вы не можете отвечать за ` другого ` пользователя!",
            ephemeral=True,
            delete_after=10
        )
        return await body.response.edit_message(
            f"# {self.emoji} Очистка"
            f"\n- {body.author.mention}, вы ` решили ` отказаться от очистки",
            view=None,
            delete_after=20
        )
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    def is_bot_messages_delete(self) -> bool:
        return self.delete_bot_messages == "Да"

    def is_user_messages_delete(self) -> bool:
        return self.mentioned_user is not None

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = 1487385743188819968

    @commands.slash_command(description="Очищает количество сообщений в чате",
     guild_ids=[1466509350100013226],
     default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def clear(self, body: disnake.ApplicationCommandInteraction,
        значение: int = commands.Param(description="Сколько очистится сообщений", le=1000),
        удалить_сообщения_ботов: str = commands.Param(
            description="Удаляет сообщения ботов, если требуется",
            choices=[
                "Да",
                "Нет"
            ],
            default="Нет"
        ),
        удалить_сообщения_пользователя: disnake.Member = commands.Param(
            description="Удаляет сообщения определённого пользователя",
            default=None
        )
    ):
        view = ClearView(self.bot, 1487385743188819968, body.author, удалить_сообщения_ботов, удалить_сообщения_пользователя)
        await body.response.send_message(
            f"# {self.bot.get_emoji(self.emoji)} Очистка"
            f"\n- {body.author.mention}, будет очищено ` {значение} ` сообщений, уверены?",
            view=view
        )
        view.clear_value = значение
        view.message = await body.original_response()

def setup(bot):
    bot.add_cog(ClearCommand(bot))
