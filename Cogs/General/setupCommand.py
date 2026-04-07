import disnake
from disnake.ext import commands
from Database import database

class SetupFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = {"Main": 1490239907103244400}

    @commands.slash_command(description="Кастомизация профиля для /menu",
                            guild_ids=[1466509350100013226])
    async def setup(
            self,
            body: disnake.ApplicationCommandInteraction,
            имя: str = commands.Param(description="Ваш псевдоним", min_length=3, max_length=30),
            возраст: int = commands.Param(description="Ваш возраст", ge=8, le=80),
            описание: str = commands.Param(description="Ваше описание", min_length=15, max_length=150),
            языки: str = commands.Param(description="Языки программировния, которые используете, через запятую", min_length=3, max_length=100, default="Нет"),
            направление: str = commands.Param(description="Ваш стек, или множество стеков", min_length=3, max_length=100, default="Нет"),
            стаж: int = commands.Param(description="Ваш опыт в IT, в годах", ge=0, le=50, default=0),
            github: str = commands.Param(description="Ваша ссылка на https://github.com", min_length=3, max_length=70, default="Не указано"),
            gitlab: str = commands.Param(description="Ваша ссылка на https://gitlab.com", min_length=3, max_length=70, default="Не указано"),
            status: str = commands.Param(description="Ваш статус, о чем думаете сегодня?", min_length=5, max_length=30, default="Нет")
            ):
        await body.response.defer(ephemeral=True)
        async with database.db.cursor() as cursor:
            await cursor.execute(
                    """
                    INSERT INTO users (user_id, user_name, user_age, user_description)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT (user_id)
                    DO UPDATE SET
                    user_name = excluded.user_name,
                    user_age = excluded.user_age, 
                    user_description = excluded.user_description
                    """,
                    (body.author.id, имя, возраст, описание)
                    )
            await cursor.execute(
                    """
                    INSERT INTO user_bio (user_id, user_langs, user_tech, user_experience, user_github, user_gitlab, user_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (user_id)
                    DO UPDATE SET
                    user_langs = excluded.user_langs,
                    user_tech = excluded.user_tech, 
                    user_experience = excluded.user_experience,
                    user_github = excluded.user_github,
                    user_gitlab = excluded.user_gitlab,
                    user_status = excluded.user_status
                    """,
                    (body.author.id, языки, направление, стаж, github, gitlab, status)
                    )
            await database.db.commit()
        await body.edit_original_response(
                f"# <a:main:{self.emojis['Main']}> Кастомизация профиля"
                "\n- Ваши настройки ` обновлены `, проверить можно в ` /menu `",
                delete_after=30
                )


def setup(bot):
    bot.add_cog(SetupFunction(bot))
