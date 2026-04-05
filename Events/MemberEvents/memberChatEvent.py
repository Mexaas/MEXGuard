from disnake.ext import commands
import disnake
from Database import database

class FirstMemberChatEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    autosetup_channels = [1476554222874132491, 1476961225127628992, 1477014878102356028]
    emojis = [1477235040084557848]
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.channel.id in self.autosetup_channels:
            async with database.db.execute(
                "SELECT join_value FROM users WHERE user_id = ?",
                (message.author.id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row and row[0] == 0:
                    return
                if not row or row[0] == 1:
                    

                    await database.db.execute(
                        """
                        INSERT INTO users (user_id, join_value)
                        VALUES (?, 0)
                        ON CONFLICT(user_id)
                        DO UPDATE SET join_value = 0
                        """,
                        (message.author.id,)
                    )
                    await database.db.commit()
                    
                    await message.channel.send(
                        f"# {self.bot.get_emoji(self.emojis[0])} Привет, {message.author.mention}!\n"
                        f"- Добро пожаловать на ` {message.guild.name} `"
                        "> Похоже ты здесь впервые 🙂"
                        "> используй ` /menu ` для полной навигации",
                        delete_after=60
                    )

def setup(bot):
    bot.add_cog(FirstMemberChatEvent(bot))
