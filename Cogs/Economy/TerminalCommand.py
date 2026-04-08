import disnake 
import asyncio 
from disnake.ext import commands
from disnake.ui import View

class Terminal_Back_Button(disnake.ui.Button):
    def __init__(self, terminal, game_emoji: dict):
        super().__init__(
                label="Домой",
                emoji=disnake.PartialEmoji(name="home", id=game_emoji["Terminal_Process_Open"]),
                style=disnake.ButtonStyle.secondary,
                row=1
                )
        self.terminal = terminal
        self.game_emoji = game_emoji
    async def callback(self, body: disnake.MessageInteraction):
        await body.response.edit_message(content=f"# <a:44503lockkey:{self.game_emoji['Terminal_Process_Open']}> Открываем...", view=None)
        await self.terminal(body)

class Terminal_Operations(disnake.ui.View):
    def __init__(self, game_emoji: dict, terminal):
        super().__init__(timeout=None)
        self.game_emoji = game_emoji
        self.terminal = terminal

        buttons = [
                {
                    "name": "BruteForce-Attack",
                    "button": disnake.ui.Button(
                        label="Брутфорс Атака",
                        emoji=disnake.PartialEmoji(
                            name="Brute-Force Attack",
                            id=self.game_emoji["Brute-Force Attack"]
                            )
                        ),
                    "callback": self.on_bruteforce_callback
                    },
                    {
                    "name": "Phishing Game",
                    "button": disnake.ui.Button(
                        label="Фишинг",
                        emoji=disnake.PartialEmoji(
                            name="Phishing Game",
                            id=self.game_emoji["Phishing Game"]
                            )
                        ),
                    "callback": self.on_phishing_callback
                    },
                    {
                    "name": "Regex Matcher",
                    "button": disnake.ui.Button(
                        label="Верный регистр",
                        emoji=disnake.PartialEmoji(
                            name="Regex Matcher",
                            id=self.game_emoji["Regex Matcher"]
                            )
                        ),
                    "callback": self.on_regex_callback
                    }

                ]
        for btn in buttons:
            button = btn["button"]

            button.callback = btn["callback"]
            self.add_item(button)

    async def on_bruteforce_callback(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
                "Вы выбрали ` Brute-Force ` атаку",
                view=view
                )
    async def on_phishing_callback(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
                "Вы выбрали ` Phishing Game `",
                view=view
                )
    async def on_regex_callback(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
                "Вы выбрали ` Regex Matcher `",
                view=view
                )


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
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
            "Вы вступили в ` Red Team `!",
            view=view
            )

    async def on_callback_blue(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
            "Вы вступили в ` Blue Team `!",
            view=view
            )

    async def on_callback_purple(self, body: disnake.MessageInteraction):
        view = View()
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
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
                    },
                    {
                    "name": "operations",
                    "button": disnake.ui.Button(
                        label="Операции",
                        emoji=disnake.PartialEmoji(
                            name="Operation_Selector",
                            id=self.game_emoji["Terminal_UI_Operations"]
                            )
                        ),
                    "callback": self.on_callback_operations
                    }
                ]
        for item in buttons:
            button = item["button"]

            button.callback = item["callback"]
            self.add_item(button)

    async def on_callback_role_select(self, body: disnake.MessageInteraction):
        view: Terminal_RoleSelect = Terminal_RoleSelect(self.game_emoji, self.terminal)
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
                f"# <a:97794computerlove:{self.game_emoji['Terminal_Main_Window']}> Выбор роли\n"
                "- ` Красные ` - хакеры, занимаются нахождением уязвимостей и взломами\n"
                "> ` Синие ` - защитники, их задача - предотвратить утечки и возможные уязвимости\n"
                "> ` Фиолетовые ` - золотая середина между красными и синими",
                view=view
                )
    async def on_callback_operations(self, body: disnake.MessageInteraction):
        view: Terminal_Operations = Terminal_Operations(self.game_emoji, self.terminal)
        view.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))
        await body.response.edit_message(
                f"# <a:97794computerlove:{self.game_emoji['Terminal_Main_Window']}> Операции\n"
                "- Список ` доступных ` операций",
                view=view
                )

class StartTerminal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_emoji = {
            "Terminal_Process_Open": 1490239885653577829,
            "Terminal_Main_Window": 1490239953970663527,
            "Terminal_UI_Role_Select": 1490239879894925503,
            "Terminal_UI_Operations": 1490239907103244400,
            "BlueTeam": 1490240057922289805,
            "RedTeam": 1490240083578716211,
            "PurpleTeam": 1490240062171123822,
            "Star": 1477235374127452160,
            "Brute-Force Attack": 1490239862857793556,
            "Phishing Game": 1491381567761678508,
            "Regex Matcher": 1491381582588678205
            }

    @commands.slash_command(description="Открывает терминал", guild_ids=[1466509350100013226])
    async def terminal(self, body: disnake.ApplicationCommandInteraction):
        view: TerminalUI = TerminalUI(self.game_emoji, self.terminal)
        if not body.response.is_done():
            await body.response.defer(ephemeral=True)
        await body.edit_original_response(
                f"# <a:lock:{self.game_emoji['Terminal_Process_Open']}> Открываем...",
                )
        await asyncio.sleep(1.2)
        await body.edit_original_response(
                f"# <a:terminal:{self.game_emoji['Terminal_Main_Window']}> Привет, {body.author.mention}!\n"
                f"- Терминал: ` открыт ` (/home/**{body.author.name}**)\n"
                "- Сторона: ` RedTeam `\n"
                "> Управляйте терминалом через ` GUI `",
                allowed_mentions=disnake.AllowedMentions.none(),
                view=view
                )

def setup(bot):
    bot.add_cog(StartTerminal(bot))
