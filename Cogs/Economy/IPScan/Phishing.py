import disnake
from disnake.ui import View
from disnake.ext import commands
from Cogs.Economy.TerminalCommand import Terminal_Back_Button

class Phishing(disnake.ui.Button):
    def __init__(self, terminal, game_emoji):
        self.terminal = terminal
        self.game_emoji = game_emoji
        super().__init__(
            label="Phishing Finder",
            style=disnake.ButtonStyle.danger,
            emoji=disnake.PartialEmoji(
               name="Phishing",
               id=game_emoji["Phishing Game"] 
            )
        )
    async def callback(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
            "Phishing",
            view=view 
        )

