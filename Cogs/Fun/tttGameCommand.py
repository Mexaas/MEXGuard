import disnake
from disnake.ext import commands

class TicTacToeButton(disnake.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(
            label="\u200B",
            style=disnake.ButtonStyle.secondary,
            row=y
        )
        self.x = x
        self.y = y
    async def callback(self, body: disnake.MessageInteraction):
        view: TicTacToeRequestView = self.view
        if body.author not in (view.player_x, view.player_o):
            return await body.response.send_message("# :x: Ошибка\n- Вы ` не участник ` игры!", ephemeral=True,
                delete_after=10
            )
        if body.author == view.current_player:
            current_cache = view.player_o if view.current_player == view.player_x else view.player_x

            mark = "❌" if view.current_player == view.player_x else "⭕"
            view.board[self.y][self.x] = mark
            self.emoji = mark
            self.disabled = True

            await body.response.edit_message(
                "# :arrow_right: Крестики-нолики\n"
                f"- Ход игрока: {current_cache.mention}",
                view=view
            )
            if view.is_draw():
                self.disable_items(view)
                return await body.edit_original_response(
                "# :candle: Ничья\n- Игра ` окончена `, никто не смог выиграть",
                view=view
            )
            if view.is_winner():
                self.disable_items(view)
                return await body.edit_original_response(
                f"# :crown: Игра окончена\n- Победитель: {view.current_player.mention}",
                view=view
            )
            view.current_player = view.player_o if view.current_player == view.player_x else view.player_x
            return
        else:
            return await body.response.send_message("# :x: Ошибка\n- Сейчас ` не ваш ` ход!", ephemeral=True,
                delete_after=10
            )
    def disable_items(self, view):
        for item in view.children:
            item.disabled = True

class TicTacToeRequestView(disnake.ui.View):
    def __init__(self, player_x: disnake.Member, player_o: disnake.Member):
        super().__init__(timeout=180)
        self.message = None
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = player_x

    def is_winner(self) -> bool:
        lines = []
        lines.extend(x for x in self.board)
        for y in range(3):
            lines.append([self.board[x][y] for x in range(3)])

        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] is not None and line.count(line[0]) == 3:
                return True
        return False
    def is_draw(self) -> bool:
        return all(index is not None for row in self.board for index in row)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.success)
    async def accept_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.player_o: return await body.response.send_message(
            "# :x: Ошибка\n- Вы не можете ` отвечать ` за другого пользователя!",
            ephemeral=True,
            delete_after=10
        )
        self.clear_items()
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(y, x))

        await body.response.send_message(
            "# :arrow_right: Крестики-нолики\n"
            f"- Ход игрока: {self.current_player.mention}"
            "\n:warning: Раунд длится ` 3 минуты `. После окончания - игра будет недоступна",
            view=self
        )
        await self.message.delete()
        self.message = await body.original_response()

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.danger)
    async def deny_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        if body.author != self.player_o: return await body.response.send_message(
            "# :x: Ошибка\n- Вы не можете ` отвечать ` за другого пользователя!",
            ephemeral=True,
            delete_after=10
        )
        await body.response.edit_message(
            f"# :x: Крестики-нолики\n- {self.player_o.mention} отказался от ` предложения ` пользователя {self.player_x.mention}!",
            view=None,
            delete_after=30
        )
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        return await self.message.edit(
            "# :small_red_triangle_down: Игра остановлена\n"
            "- Игра длилась ` 3 минуты ` и не была завершена",
            delete_after=30,
            view=self
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
                    f"\nУ вас ` 60 ` секунд, чтобы с делать выбор",
                    view=view,
                    delete_after=60
                )
                view.message = await body.original_response()

def setup(bot):
    bot.add_cog(TicTacToeCommand(bot))
