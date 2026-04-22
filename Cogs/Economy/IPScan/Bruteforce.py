import disnake
from disnake.ui import View
from disnake.ext import commands, tasks

class BruteForceGameLogic(disnake.ui.View):
    def __init__(self, terminal, game_emoji,
                 player: disnake.Member,
                 message_default_tick: int
            ):
        super().__init__(timeout=300) 
        self.player = player
        self.progress = 0
        self.heap = 0
        self.message = None
        self.message_update.change_interval(seconds=message_default_tick)

    @tasks.loop(seconds=1.0)
    async def message_update(self):
        if not self.message:
            return
        content = (
            f"Прогресс: {self.progress} / 100 ` % `\n"
            f"Прогресс криминала (IDS): {self.heap} / 100 ` % `"
        )
        try:
            await self.message.edit(content=content, view=self)
        except disnake.NotFound:
            self.stop_game()

    def stop_game(self):
        self.message_update.cancel()
        self.stop()

    @disnake.ui.button(label="Ебашить быстрее", style=disnake.ButtonStyle.danger)
    async def on_up_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        self.progress += 5
        self.heap += 15 
        await body.response.send_message("Скорость потоков увеличена!", ephemeral=True)

    @disnake.ui.button(label="Замедлить атаку", style=disnake.ButtonStyle.success)
    async def on_down_click(self, button: disnake.ui.Button, body: disnake.MessageInteraction):
        self.heap -= 10
        if self.heap < 0: self.heap = 0
        await body.response.send_message("Залегли на дно. Подозрение падает...", ephemeral=True)


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
        view = BruteForceGameLogic(self.terminal, self.game_emoji, body.author, 3)
        
        await body.response.edit_message(content="Запуск модулей взлома...", view=view)
        view.message = await body.original_message() 
        view.message_update.start()
