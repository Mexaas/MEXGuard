import disnake
from disnake.ext import commands
from Database import database
class SyncUsersCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Синхронизирует всех пользователей с БД", guild_ids=[1466509350100013226],
        default_member_permissions=disnake.Permissions(administrator=True))
    async def sync(self, body: disnake.ApplicationCommandInteraction):
        await body.response.defer(ephemeral=True)
        for user in body.guild.members:
            await database.setup_user(user.id, user.display_name)
            print(
                f"{user.display_name} зарегистрирован"
            )
        await database.db.commit()
        await body.followup.send(
            "# :inbox_tray: Отлично!\n- Все пользователи ` синхронизированы `!"
            "\n> Значения взяты как ` базовые ` и подставлены под каждого пользователя",
            delete_after=10
        )

def setup(bot):
    bot.add_cog(SyncUsersCommand(bot))
