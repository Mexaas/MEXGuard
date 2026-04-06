import disnake 
import asyncio 
from disnake.ext import commands
from disnake.ui import View

class Terminal_Back_Button(disnake.ui.Button):
    def __init__(self, terminal):
        super().__init__(
                label="Домой",
                style=disnake.ButtonStyle.secondary,
                row=1
                )
        self.terminal = terminal
    async def callback(self, body: disnake.MessageInteraction):
        await self.terminal(body)

class Terminal_RoleSelect(disnake.ui.View):
    def __init__(self, game_emoji: dict, terminal):
        super().__init__(timeout=None)
        self.game_emoji = game_emoji
        self.terminal = terminal

        buttons = [
                    {
                    "name": "red_role",
                    "button": disnake.ui.Button(
                        label="Красные",
                        emoji=disnake.PartialEmoji(
                            name="Red_Selector",
                            id=self.game_emoji["RedTeam"]
                            ),
                        style=disnake.ButtonStyle.danger
                        ),
                    "callback": self.on_callback_red
                    },
                    {       
                    "name": "blue_role",
                    "button": disnake.ui.Button(
                        label="Синие",
                        emoji=disnake.PartialEmoji(
                            name="Blue_Selector",
                            id=self.game_emoji["BlueTeam"]
                            ),
                        style=disnake.ButtonStyle.primary
                        ),
                    "callback": self.on_callback_blue
                    },
                    {
                    "name": "purple_role",
                    "button": disnake.ui.Button(
                        label="Фиолетовые",
                        emoji=disnake.PartialEmoji(
                            name="Purple_Selector",
                            id=self.game_emoji["PurpleTeam"]
                            ),
                        style=disnake.ButtonStyle.secondary
                        ),
                    "callback": self.on_callback_purple
                    }
                ]
        for item in buttons:
            button = item["button"]

            button.callback = item["callback"]
            self.add_item(button)

    async def on_callback_red(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal))
        await body.response.edit_message(
            "Вы вступили в ` Red Team `!",
            view=view
            )

    async def on_callback_blue(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal))
        await body.response.edit_message(
            "Вы вступили в ` Blue Team `!",
            view=view
            )

    async def on_callback_purple(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal))
        await body.response.edit_message(
            "Вы вступили в ` Purple Team `!",
            view=view
            )

class TerminalUI(disnake.ui.View):
    def __init__(self, game_emoji: dict, terminal):
        super().__init__(timeout=None)
        self.game_emoji = game_emoji
        self.terminal = terminal

        buttons = [
                    {
                    "name": "role_select",
                    "button": disnake.ui.Button(
                        label="Выбрать роль",
                        emoji=disnake.PartialEmoji(
                            name="Role_Selector",
                            id=self.game_emoji["Terminal_UI_Role_Select"]
                            )
                        ),
                    "callback": self.on_callback_role_select
                    }
                ]
        for item in buttons:
            button = item["button"]

            button.callback = item["callback"]
            self.add_item(button)

    async def on_callback_role_select(self, body: disnake.MessageInteraction):
        view: Terminal_RoleSelect = Terminal_RoleSelect(self.game_emoji, self.terminal)
        view.add_item(Terminal_Back_Button(self.terminal))
        await body.response.edit_message(
                f"# {await body.guild.fetch_emoji(self.game_emoji['Terminal_Main_Window'])} Выбор роли\n"
                "- ` Красные ` - хакеры, занимаются нахождением уязвимостей и взломами\n"
                "> ` Синие ` - защитники, их задача - предотвратить утечки и возможные уязвимости\n"
                "> ` Фиолетовые ` - золотая середина между красными и синими",
                view=view
                )


class StartTerminal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_emoji = {
            "Terminal_Process_Open": 1490239885653577829,
            "Terminal_Main_Window": 1490239953970663527,
            "Terminal_UI_Role_Select": 1490239879894925503,
            "BlueTeam": 1490240057922289805,
            "RedTeam": 1490240083578716211,
            "PurpleTeam": 1490240062171123822
            }

    @commands.slash_command(description="Открывает терминал", guild_ids=[1466509350100013226])
    async def terminal(self, body: disnake.ApplicationCommandInteraction):
        view: TerminalUI = TerminalUI(self.game_emoji, self.terminal)
        await body.response.send_message(
                f"# {self.bot.get_emoji(self.game_emoji['Terminal_Process_Open'])} Открываем...",
                ephemeral=True
                )
        await asyncio.sleep(2)
        await body.edit_original_response(
                f"# {self.bot.get_emoji(self.game_emoji['Terminal_Main_Window'])} Привет, {body.author.mention}!\n"
                f"- Терминал: ` открыт ` (/home/**{body.author.name}**)\n"
                "- Сторона: ` RedTeam `\n"
                "> Управляйте терминалом через ` GUI `",
                allowed_mentions=disnake.AllowedMentions.none(),
                view=view
                )
        view.message = await body.original_response()

def setup(bot):
    bot.add_cog(StartTerminal(bot))
