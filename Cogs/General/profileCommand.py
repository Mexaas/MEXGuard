import disnake 
from disnake.ext import commands
from Database import database

class ProfileFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = {"Main": 1490239885653577829}

    @commands.slash_command(description="Просмотр чужих профилей",
                            guild_ids=[1466509350100013226])
    async def profile(self, body: disnake.ApplicationCommandInteraction, пользователь: disnake.Member):
        if пользователь.bot or пользователь == body.author:
            return await body.response.send_message(
                    f"# :x:\n- Введите параметры команды ` правильно `!",
                    ephemeral=True,
                    delete_after=10
                    )
        await body.response.defer(ephemeral=True)
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
            (пользователь.id,)
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
                f"# {self.bot.get_emoji(self.emojis['Main'])} Профиль {пользователь.mention}\n"
                f"- Имя: ` {user_name} `\n"
                f"> Возраст: ` {user_age} `\n"
                f"> Обо мне: ` {user_description} `\n\n"
                f"- Уровень: ` {user_level} ({user_exp} exp) `\n"
                f"> Звезды: ` {user_stars} `\n"
                f"> Достижения: ` {user_achievements} `\n"
                f"> Роль уровня: {role}\n\n"
                f"- Язык: ` {user_langs} `\n"
                f"> Направление: ` {user_tech} `\n"
                f"> Стаж: ` {user_experience} ` лет\n"
                f"> Github: ` {user_github} `\n"
                f"> Gitlab: ` {user_gitlab} `\n"
                f"> Статус: ` {user_status} `\n"
            ),
            allowed_mentions=disnake.AllowedMentions.none()
        )

def setup(bot):
    bot.add_cog(ProfileFunction(bot))
