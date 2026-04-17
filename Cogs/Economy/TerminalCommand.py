import asyncio 
import disnake
import random
from disnake.ext import commands
from disnake.ui import View
import importlib

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

class TerminalUI(disnake.ui.View):
    def __init__(self, game_emoji: dict, terminal):
        super().__init__(timeout=None)
        self.game_emoji = game_emoji
        self.terminal = terminal

        buttons = [
                   {
                    "name": "scan",
                    "button": disnake.ui.Button(
                        label="Сканирование IP",
                        emoji=disnake.PartialEmoji(
                            name="ipscan",
                            id=self.game_emoji["Brute-Force Attack"]
                            )
                        ),
                    "callback": self.on_callback_ipscan
                    }
                ]
        for item in buttons:
            button = item["button"]

            button.callback = item["callback"]
            self.add_item(button)

    async def on_callback_ipscan(self, body: disnake.MessageInteraction):
        files = ["Bruteforce", "Phishing", "Regex"]
        game = [
            {
                "difficulty": "Лёгкая",
                "ip": "192.168."
            },
            {
                "difficulty": "Средняя",
                "ip": "10."
            },
            {
                "difficulty": "Сложная",
                "ip": "6."
            },
        ]
        scan_phases = [
            "Определение маршрута трафика",
            "Анализ TTL",
            "Поиск открытых портов",
            "Поиск уязвимостей для входа",
            "Сбор данных подсети",
            "Попытка сбора информации"
        ]
        view = View()
        template = random.choice(game)
        template_ip = template["ip"]
        difficulty = template["difficulty"]
        ip = ".".join([str(random.randint(0, 255)) for _ in range(4 - template_ip.count("."))])

        await body.response.edit_message(
            f"# <a:terminal:{self.game_emoji['Terminal_Main_Window']}> Инициализация\n"
            "- Начинается ` сканирование ` и поиск жертвы...\n"
            "> Есть ` 3 ` вида сложностей: чем опаснее, тем вас ` проще ` обнаружить",
            view=None
        )
        objects = await self.sync_game_buttons(files, "Cogs.Economy.IPScan.")
        await self.buttons_add(objects, view)

        await asyncio.sleep(4)
        for _ in range(3, random.randint(7, 10)):
            await asyncio.sleep(random.randint(1, 2))
            await body.edit_original_response(
                f"# <a:load:{self.game_emoji['Loading']}> {random.choice(scan_phases)}" 
            )
        await body.edit_original_response(
            f"# <a:success:{self.game_emoji['Lamp']}> Найден IP\n"
            f"- Жертва: ` {template_ip + ip} `\n" 
            f"> Сложность: ` {difficulty} `",
            view=view
        )

    async def sync_game_buttons(self, files: list, path: str) -> list:
        objects = []
        for name in files:
            module = importlib.import_module(path + name)
            
            objects.append(getattr(module, name))
        return objects

    async def buttons_add(self, objects: list, view):
        for object in objects:
            view.add_item(object(self.terminal, self.game_emoji))

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
            "Regex Game": 1491381582588678205,
            "Loading": 1490239840149573814,
            "Lamp": 1491381518185271327,
            "ArrowRight": 1491381384919515358
            }

    @commands.slash_command(description="Открывает терминал", guild_ids=[1466509350100013226])
    async def terminal(self, body: disnake.ApplicationCommandInteraction):
        admin_id = 798769818068713492
        if body.author.id != admin_id:
            return await body.response.send_message("# :x: Ошибка\n- Отказано в ` доступе `", ephemeral=True)

        view: TerminalUI = TerminalUI(self.game_emoji, self.terminal)
        if not body.response.is_done():
            await body.response.defer(ephemeral=True)
        await body.edit_original_response(
                f"# <a:lock:{self.game_emoji['Terminal_Process_Open']}> Открываем...",
                )
        await asyncio.sleep(1.2)
        await body.edit_original_response(
                f"# <a:terminal:{self.game_emoji['Terminal_Main_Window']}> Привет, {body.author.mention}!\n"
                f"- Терминал: ` открыт `\n"
                f"> ` /home/{body.author.name} ` <a:right:{self.game_emoji['ArrowRight']}> ` {body.author.name}@{body.author.name}: `",
                allowed_mentions=disnake.AllowedMentions.none(),
                view=view
                )

def setup(bot):
    bot.add_cog(StartTerminal(bot))

