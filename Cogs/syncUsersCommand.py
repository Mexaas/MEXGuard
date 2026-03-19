import disnake
from disnake.ext import commands
from Database.database import db

class SyncUsersCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Синхронизирует всех пользователей с БД", guild_ids=[1466509350100013226])
    async def sync(self, body: disnake.ApplicationCommandInteraction):
        await body.response.defer()
        for user in body.guild.members:
            await db.execute(
                """
                INSERT INTO users(user_id, user_name, user_age, user_description)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE
                SET user_age = excluded.user_age,
                    user_name = excluded.user_name,
                    user_description = excluded.user_description
                """,
                (user.id, "Не указано", 16, "Не указано")
            )
            await db.execute(
                """
                INSERT INTO user_stats(user_id, user_level, user_level_role, user_exp, user_stars)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE
                SET user_level = excluded.user_level,
                    user_level_role = excluded.user_level_role,
                    user_exp = excluded.user_exp,
                    user_stars = excluded.user_stars
                """,
                (user.id, 0, 12345, 0, 0)
            )
            await db.execute(
                """
                INSERT INTO user_bio(user_id, user_langs, user_tech,
                user_experience, user_status, user_github, user_gitlab, user_achievements)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE
                SET user_langs = excluded.user_langs,
                    user_tech = excluded.user_tech,
                    user_experience = excluded.user_experience,
                    user_status = excluded.user_status,
                    user_github = excluded.user_github,
                    user_gitlab = excluded.user_gitlab,
                    user_achievements = excluded.user_achievements
                """,
                (user.id, "Нет", "Нет", 0, "Нет", "Нет", "Нет", "Нет")
            )
        await db.commit()
        await body.response.send_message(
            "# :inbox_tray: Отлично!\n- Все пользователи ` синхронизированы `!"
            "\n> Значения взяты как ` базовые ` и подставлены под каждого пользователя",
            ephemeral=True,
            delete_after=10
        )

def setup(bot):
    bot.add_cog(SyncUsersCommand(bot))
