import disnake
from disnake.ext import commands

class TicTacToeButton(disnake.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(
            label="\u200B",
            style=disnake.ButtonStyle.secondary,
            row=x
        )
        self.x = x
        self.y = y
    async def callback(self, body: disnake.MessageInteraction):
        view: TicTacToeRequestView = self.view
        if body.author not in (view.player_x, view.player_o):
            return await body.response.send_message("Вы не участник игры!", ephemeral=True)

        if body.author == view.current_player:
            view.current_player = view.player_o if view.current_player == view.player_x else view.player_x
            mark = "❌" if view.current_player == view.player_x else "⭕"
            self.emoji = mark
            self.disabled = True
            return await body.response.edit_message(
                "# :arrow_right: Крестики-нолики\n"
                f"- Ход игрока: {view.current_player.mention}",
                view=view
            )
        await body.response.send_message("Сейчас не ваш ход!", ephemeral=True)

class TicTacToeRequestView(disnake.ui.View):
    def __init__(self, player_x: disnake.Member, player_o: disnake.Member):
        super().__init__(timeout=120)
        self.message = None
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = self.player_x

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.success)
    async def accept_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.player_o: return await body.response.send_message(
            "# :x: Ошибка\n- Вы не можете ` отвечать ` за другого пользователя!",
            ephemeral=True,
            delete_after=10
        )
        self.clear_items()
        for row in range(3):
            for column in range(3):
                self.add_item(TicTacToeButton(row, column))
        await body.response.edit_message(
            "# :arrow_right: Крестики-нолики\n"
            f"- Ход игрока: {self.current_player.mention}",
            view=self
        )

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.danger)
    async def deny_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.player_o: return await body.response.send_message(
            "# :x: Ошибка\n- Вы не можете ` отвечать ` за другого пользователя!",
            ephemeral=True,
            delete_after=10
        )
        await body.response.edit_message(
            f"# :x: Крестики-нолики\n- {self.player_o.mention} отказался от ` предложения ` пользователя {self.player_x.mention}!",
            view=None
        )
    async def on_timeout(self):
        return await self.message.edit(
            "# :x: Время вышло\n- Пользователь ` не дал ` ответ на предложение!",
            delete_after=20, view=None
        )

class TicTacToeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Сыграть в крестики-нолики", guild_ids=[1466509350100013226])
    async def tictactoe(self, body: disnake.ApplicationCommandInteraction, пользователь: disnake.Member):
        match пользователь.id:
            case body.author.id: return await body.response.send_message(
                "# :x: Ошибка\n- Вы не можете вызвать ` себя ` на игру!",
                ephemeral=True, delete_after=15
            )
            case self.bot.user.id: return await body.response.send_message(
                "# :x: Ошибка\n- Вы не можете вызвать ` бота ` на игру!",
                ephemeral=True, delete_after=15
            )
            case _:
                view = TicTacToeRequestView(body.author, пользователь)
                await body.response.send_message(
                    f"# :clock2: Крестики-нолики\n- {пользователь.mention}, хотите ` сыграть ` с {body.author.mention}?"
                    f"\n> У вас ` 10 ` секунд, чтобы с делать выбор",
                    view=view
                )
                view.message = await body.original_response()

def setup(bot):
    bot.add_cog(TicTacToeCommand(bot))
