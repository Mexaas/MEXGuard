import disnake
from disnake.ext import commands
import random
import asyncio

class AgainRequestView(disnake.ui.View):
    def __init__(self, message, author: disnake.Member, repeat_function):
        super().__init__(timeout=20)
        self.message = message
        self.author = author
        self.repeat_function = repeat_function

    @disnake.ui.button(label="Повторить")
    async def on_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.author:
            return await body.response.send_message("# :x: Ошибка\n- Вы не можете ` использовать ` эту кнопку!", ephemeral=True)
        await self.message.delete()
        await self.repeat_function(body)

class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_emoji = 1489947752992608359
        self.game_choices = ["Решка", "Орёл"]

    @commands.slash_command(
        description="Бросает монетку",
        guild_ids=[1466509350100013226]
    )
    async def coinflip(self, body: disnake.ApplicationCommandInteraction):
        emoji = self.bot.get_emoji(self.game_emoji)
        await body.response.send_message(
            f"# {emoji} Бросаю для вас монетку, {body.author.mention}!"
        )
        view = AgainRequestView(await body.original_response(), body.author, self.coinflip)
        await asyncio.sleep(1)
        await body.edit_original_response(f"# {emoji} Монетка летит...")

        await asyncio.sleep(2)
        result = random.choice(self.game_choices)
        await body.edit_original_response(
            f"# {emoji} Монетка" + "\n- Выпала ` решка `" if result == "Решка" else
            f"# {emoji} Монетка" + "\n- Выпал ` орёл `",
            delete_after=20,
            view=view
        )

def setup(bot):
    bot.add_cog(CoinflipCommand(bot))
