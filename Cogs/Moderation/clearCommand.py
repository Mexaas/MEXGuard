import disnake
import asyncio
from disnake.ext import commands

class ClearView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.clear_value = None
        self.message = None

    @disnake.ui.Button(label="Подтвердить", style=disnake.ButtonStyle.success)
    async def accept_callback(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        await self.message.edit(
            f"# {self.bot.get_emoji(self.emojis[0])} Очистка"
            f"\n- Сжираю ` {self.clear_value} ` сообщений...",
            view=None
        )
        await body.channel.purge(
            limit=self.clear_value
        )
        await asyncio.sleep(2)
        return await self.message.edit(
            f"# {self.bot.get_emoji(self.emojis[0])} Очистка"
            f"\n- Съел ` {self.clear_value} ` сообщений. Было очень вкусно",
            view=None,
            delete_after=20
        )

    @disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger)
    async def deny_callback(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        return await self.message.edit(
            f"# {self.bot.get_emoji(self.emojis[0])} Очистка"
            "\n- Вы ` решили ` отказаться от очистки",
            view=None,
            delete_after=20
        )

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [1487385743188819968]

    @commands.slash_command(description="Очищает количество сообщений в чате",
     guild_ids=[1466509350100013226],
     default_member_permissions=disnake.Permissions(administrator=True)
    )
    async def clear(self, body: disnake.ApplicationCommandInteraction,
        значение: int = commands.Param(description="Сколько очистится сообщений", le=1000)
    ):
        view = ClearView()
        await body.response.send_message(
            f"# {self.bot.get_emoji(self.emojis[0])} Очистка"
            f"\n- Будет очищено ` {значение} ` сообщений, уверены?",
            view=view
        )
        view.clear_value = значение
        view.message = await body.original_response()

def setup(bot):
    bot.add_cog(ClearCommand(bot))
