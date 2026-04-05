import disnake
from disnake.ext import commands
from pathlib import Path
from Database import database

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
            ),
            disnake.SelectOption(
                label="Кастомизация ролей", emoji="🎨",
                description="Выбери роль для себя", value="roles"
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
                "- /remove_thread || Удаляет ветку, если вы владелец ||\n"
                "> /coinflip || Бросает монетку ||\n"
                "> /tictactoe || Крестики-нолики ||\n"
                "> /menu || Навигация ||",
                ephemeral=True,
                file=self.get_image("commands"),
                view=view
            )
            view.message = await body.original_message()
            return
        elif self.values[0].__contains__("profile"):
            await body.response.defer()
            view = DropDownSelect()
            async with database.db.execute(
                """
                SELECT
                    u.user_name,
                    u.user_age,
                    u.user_description,
                    s.user_level,
                    s.user_level_role,
                    s.user_exp,
                    s.user_stars,
                    b.user_langs,
                    b.user_tech,
                    b.user_experience,
                    b.user_status,
                    b.user_github,
                    b.user_gitlab,
                    b.user_achievements
                FROM users u
                LEFT JOIN user_stats s ON u.user_id = s.user_id
                LEFT JOIN user_bio b ON u.user_id = b.user_id
                WHERE u.user_id = ?
                """,
                (body.author.id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                user_name = body.author.display_name
                user_age = user_description = user_level_role = "Нет"
                user_level = 0; user_exp = 0; user_stars = 0
                user_langs = user_tech = user_gitlab = user_status = "Нет"
                user_experience = user_github = user_achievements = "Нет"
            else:
                (user_name,
                    user_age, user_description, user_level,
                    user_level_role, user_exp, user_stars,
                    user_langs, user_tech, user_experience,
                    user_status, user_github,
                    user_gitlab, user_achievements
                ) = row
            role = (await body.guild.fetch_role(user_level_role)).mention if isinstance(user_level_role, int) else "` Нет `"
            await body.followup.send(
                content=(
                    f"## {await body.guild.fetch_emoji(self.emojis[4])} Пользователь\n"
                    f"> Имя: ` {user_name} `\n"
                    f"> Возраст: ` {user_age} `\n"
                    f"- Обо мне: ` {user_description} `\n\n"
                    f"## {await body.guild.fetch_emoji(self.emojis[4])} Статистика\n"
                    f"> Уровень: ` {user_level} ({user_exp} exp) `\n"
                    f"> Звезды: ` {user_stars} `\n"
                    f"> Достижения: ` {user_achievements} `\n"
                    f"- Роль уровня: {role}\n\n"
                    f"## {await body.guild.fetch_emoji(self.emojis[4])} Деятельность\n"
                    f"> Язык: ` {user_langs} `\n"
                    f"> Направление: ` {user_tech} `\n"
                    f"> Стаж: ` {user_experience} `\n"
                    f"> Github: ` {user_github} `\n"
                    f"> Gitlab: ` {user_gitlab} `\n"
                    f"- Статус: ` {user_status} `\n"
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
                f"# {await body.guild.fetch_emoji(self.emojis[0])} Правила сервера\n"
                f"- Уважайте ` пользователей ` сервера — ` оскорбления `, ` травля `, ` токсичность `, ` провокации `, ` дискриминация ` запрещены\n"
                f">    Запрещается flood, caps, spam и реклама, кроме ` github.com ` или ` gitlab.com `\n"
                f">    Запрещается ` любой обход ` правил или ограничений\n"
                f">    Багоюз/абьюз ` механик ` сервера в злоумышленных целях запрещён\n"
                f">    Накрутка активностей (` фарм XP `, ` твинк-аккаунты ` и т.п.) запрещена\n"
                f">    Публикация ` вредоносного ` контента или материалов, которые могут ` навредить ` пользователям или серверу, запрещена\n"
                f">    Запрещён ` слив личной ` информации, докс, угрозы и шантаж\n"
                f">    Запрещён ` шок-контент `, ` NSFW ` и ` незаконные ` материалы\n"
                f">    Запрещена выдача себя за администрацию или других пользователей\n"
                f">    Решения модерации ` не обсуждаются в чатах `, только в ЛС у вышестоящих лиц\n",
                ephemeral=True,
                file=self.get_image("rules"),
                view=view
            )
            view.message = await body.original_message()
            return

        if self.values[0] == "roles":
            ROLES_CONFIG = [
                {"label": "Python", "value": "1476989262955020461", "e_id": 1476965625665425682, "e_name": "python"},
                {"label": "C++", "value": "1476989264683077704", "e_id": 1476966430581850245, "e_name": "cpp"},
                {"label": "C#", "value": "1476989265476063446", "e_id": 1476966552858267699, "e_name": "csharp"},
                {"label": "C", "value": "1476989267145134200", "e_id": 1476967440683372654, "e_name": "c"},
                {"label": "Java", "value": "1476989267782926448", "e_id": 1476965671022759957, "e_name": "java"},
                {"label": "JavaScript", "value": "1476989269225771151", "e_id": 1476964774050005012, "e_name": "javascript"},
                {"label": "Kotlin", "value": "1476989523022970993", "e_id": 1476965607990624490, "e_name": "kotlin"},
                {"label": "GO", "value": "1476989523660505139", "e_id": 1476968391309918261, "e_name": "go"},
                {"label": "Swift", "value": "1476989524205637693", "e_id": 1476968873260744715, "e_name": "swift"},
                {"label": "Ruby", "value": "1476989919435161804", "e_id": 1476966492129067071, "e_name": "ruby"},
                {"label": "Rust", "value": "1476989920672354304", "e_id": 1476966028889030806, "e_name": "rust"},
                {"label": "Assembly", "value": "1476989921439781086", "e_id": 1476970448385478658, "e_name": "assembly"},
                {"label": "Fortran", "value": "1476989922702393497", "e_id": 1476970922224386192, "e_name": "fortran"},
                {"label": "Dart", "value": "1476989923125891173", "e_id": 1476970237693005915, "e_name": "dart"},
                {"label": "Perl", "value": "1476989923964878858", "e_id": 1476970558527897610, "e_name": "perl"},
                {"label": "Scala", "value": "1476989926338855092", "e_id": 1476970772978335795, "e_name": "scala"},
                {"label": "Elixir", "value": "1476989926628261949", "e_id": 1476970110534160530, "e_name": "elixir"},
                {"label": "Bash", "value": "1476990393232134277", "e_id": 1476965637002891284, "e_name": "bash"},
                {"label": "Lua", "value": "1476990394154746020", "e_id": 1476968706444754995, "e_name": "lua"},
                {"label": "TypeScript", "value": "1476990394863714565", "e_id": 1476969183618269488, "e_name": "typescript"},
                {"label": "Full-Stack", "value": "1476989272962891888", "emoji": "🌐"},
                {"label": "Back-End", "value": "1476989270194389103", "emoji": "🔐"},
                {"label": "Front-End", "value": "1476989273789038896", "emoji": "🚀"},
                {"label": "Linux", "value": "1476989260753272834", "e_id": 1477007071672012861, "e_name": "linux"},
                {"label": "Windows", "value": "1476989260086120553", "e_id": 1477007253176586362, "e_name": "windows"}
            ]
            view = disnake.ui.View(timeout=60)

            role_options = []
            for r in ROLES_CONFIG:
                emoji = r.get("emoji") or disnake.PartialEmoji(name=r["e_name"], id=r["e_id"])
                role_options.append(disnake.SelectOption(label=r["label"], value=r["value"], emoji=emoji))

            select = disnake.ui.StringSelect(
                placeholder="Выберите роли",
                min_values=1,
                max_values=len(role_options),
                options=role_options
            )

            async def role_callback(body: disnake.MessageInteraction):
                selected_ids = [int(val) for val in select.values]
                author_role_ids = [r.id for r in body.author.roles]
                all_config_ids = [int(r["value"]) for r in ROLES_CONFIG]

                to_remove = []
                to_add = []

                for rid in all_config_ids:
                    if rid in author_role_ids and rid not in selected_ids:
                        role = body.guild.get_role(rid)
                        if role: to_remove.append(role)
                    elif rid not in author_role_ids and rid in selected_ids:
                        role = body.guild.get_role(rid)
                        if role: to_add.append(role)

                if to_remove: await body.author.remove_roles(*to_remove)
                if to_add: await body.author.add_roles(*to_add)

                await body.response.send_message(f"# {await body.guild.fetch_emoji(self.emojis[4])} Кастомизация ролей\n- Ваши ` роли ` обновлены!", ephemeral=True)

            select.callback = role_callback
            view.add_item(select)

            await body.response.send_message(
                f"# {await body.guild.fetch_emoji(self.emojis[4])} Кастомизация ролей\nВыберите роль ниже",
                ephemeral=True, view=view
            )

class DropDownSelect(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
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
