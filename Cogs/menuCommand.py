import disnake
from disnake.ext import commands
from pathlib import Path

class SelectMenu(disnake.ui.StringSelect):
    def __init__(self):
        self.image_type = {
            "profile": "Content/Profile_Image.png",
            "commands": "Content/Commands_Image.png",
            "rules": "Content/Rules_Image.png",
            "information": "Content/Information_Image.png"
        }
        self.emojis = [1477235374127452160, 1477235040084557848, 1476970558527897610, 1476967440683372654, 1477684758971551896]
        options=[
            disnake.SelectOption(
                label="Доступные команды", emoji="⚙️", description="Список всего функционала",
                value="help"
            ),
            disnake.SelectOption(
                label="Правила сервера", emoji="📚", description="Основные правила сервера",
                value="rules"
            ),
            disnake.SelectOption(
                label="Мой профиль", emoji="👩‍💻", description="Вся информация о тебе",
                value="profile"
            )
        ]
        super().__init__(
            placeholder="Нажмите, чтобы выбрать",
            min_values=1,
            max_values=1,
            options=options
        )

    def get_image(self, value: str) -> disnake.File:
        return disnake.File(self.image_type[value], Path(self.image_type[value]).name)

    async def callback(self, body: disnake.MessageInteraction):
        if self.values[0].__contains__("help"):
            view = DropDownSelect()
            view.message
            await body.response.send_message(
                f"# {await body.guild.fetch_emoji(self.emojis[0])} Команды\n"
                "- /remove_thread || Удаляет ветку, если вы владелец ||",
                ephemeral=True,
                file=self.get_image("commands"),
                view=view
            )
            view.message = await body.original_message()
            return
        elif self.values[0].__contains__("profile"):
            view = DropDownSelect()
            await body.response.send_message(
                content=(
                    f"## {await body.guild.fetch_emoji(self.emojis[4])} Пользователь\n"
                    f"> Имя: ` Нет `\n"
                    f"> Возраст: ` 17 `\n"
                    f"- Обо мне: ` Нет `\n\n"
                    f"## {await body.guild.fetch_emoji(self.emojis[4])} Деятельность\n"
                    f"> Язык: ` Нет `\n"
                    f"> Направление: ` Нет `\n"
                    f"> Стаж: ` 0 `\n"
                    f"> Github: ` Нет `\n"
                    f"- Статус: ` Нет `\n"

                ), 
                file=self.get_image("profile"),
                view=view,
                ephemeral=True
            )
            view.message = await body.original_message()
            return
        elif self.values[0].__contains__("rules"):
            view = DropDownSelect()
            await body.response.send_message(
                f"## {await body.guild.fetch_emoji(self.emojis[0])} Правила сервера\n"
                f"- Уважайте ` пользователей ` сервера — ` оскорбления `, ` травля `, ` токсичность `, ` провокации `, ` дискриминация ` запрещены\n"
                f">   Запрещается flood, caps, spam и реклама, кроме ` github.com ` или ` gitlab.com `\n"
                f">   Запрещается ` любой обход ` правил или ограничений\n"
                f">   Багоюз/абьюз ` механик ` сервера в злоумышленных целях запрещён\n"
                f">   Накрутка активностей (` фарм XP `, ` твинк-аккаунты ` и т.п.) запрещена\n"
                f">   Публикация ` вредоносного ` контента или материалов, которые могут ` навредить ` пользователям или серверу, запрещена\n"
                f">   Запрещён ` слив личной ` информации, докс, угрозы и шантаж\n"
                f">   Запрещён ` шок-контент `, ` NSFW ` и ` незаконные ` материалы\n"
                f">   Запрещена выдача себя за администрацию или других пользователей\n"
                f">   Решения модерации ` не обсуждаются в чатах `, только в ЛС у вышестоящих лиц\n",
                ephemeral=True,
                file=self.get_image("rules"),
                view=view
            )
            view.message = await body.original_message()
            return

class DropDownSelect(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=45)
        self.add_item(SelectMenu())
        self.message = None

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(
                f"# {await self.message.guild.fetch_emoji(1477235374127452160)} Сообщение неактивно\n"
                "- Данное окно посчиталось неактивным, и было скрыто\n"
                ">   Если вы ` хотите ` продолжить ` пользоваться ` окном,\n"
                ">   просто перевызовите его через ` /menu `",
                view=self
            )

class MenuCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = [1477235042475315240]
        self.image_type = {
            "main_menu": "Content/MenuCommand_Image.png"
        }

    def get_image(self, value: str) -> disnake.File:
        return disnake.File(self.image_type[value], Path(self.image_type[value]).name)

    @commands.slash_command(description="Навигационная команда", guild_ids=[1466509350100013226])
    async def menu(self, body: disnake.ApplicationCommandInteraction):
        view = DropDownSelect()
        await body.response.send_message(
            f"""
            # {self.bot.get_emoji(self.emojis[0])} Центр навигации
            - Выбери нужную категорию в ` селекторе ` ниже
            """,
            ephemeral=True,
            view=view,
            file=self.get_image("main_menu")
        )
        view.message = await body.original_message()
        return
    
def setup(bot):
    bot.add_cog(MenuCommand(bot))