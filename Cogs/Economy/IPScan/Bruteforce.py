import disnake
from disnake.ui import View
from disnake.ext import commands, tasks
from Cogs.Economy.TerminalCommand import Terminal_Back_Button

class BruteForceGameLogic(disnake.ui.View):
    def __init__(self, terminal, game_emoji,
                 player: disnake.Member,
                 progress_default_tick: int,
                 heap_default_tick: int,
                 message_default_tick: int
            ):
        super().__init__(timeout=None)
        self.player = player
        self.progress = 0
        self.heap = 0
        self.progress_update_tick = 1
        self.heap_update_tick = 1
        self.message_update_tick = 1

    @disnake.ui.button(
        label="Ебашить быстрее",
        style=disnake.ButtonStyle.danger
    )
    async def on_up_click(self, body: disnake.MessageInteraction):
        await body.response.send_message("up", ephemeral=True)

    @disnake.ui.button(
        label="Замедлить атаку",
        style=disnake.ButtonStyle.success
    )
    async def on_down_click(self, body: disnake.MessageInteraction):
        await body.response.send_message("down", ephemeral=True)


    @tasks.loop(seconds=message_default_tick)
    async def message_update(self, body: disnake.MessageInteraction):
        await body.response.edit_message(
            f"Прогресс: {self.progress} / 100 ` % `"
            f"Прогресс криминала: {self.heap} / 100 ` % `",
            view=self
        )


class Bruteforce(disnake.ui.Button):
    def __init__(self, terminal, game_emoji):
        self.terminal = terminal
        self.game_emoji = game_emoji
        super().__init__(
            label="Bruteforce",
            style=disnake.ButtonStyle.success,
            emoji=disnake.PartialEmoji(
               name="Bruteforce",
               id=game_emoji["Brute-Force Attack"] 
            )
        )
    async def callback(self, body: disnake.MessageInteraction):
        view = BruteForceGameLogic(self.terminal, self.game_emoji, body.author, 1,1,1)
        await body.response.edit_message(
            "BruteForce",
            view=view 
        )
