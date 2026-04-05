import disnake
from disnake.ext import commands
from Database import database

class addThreadMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    channel_ids = [1477014878102356028, 1476962126684749965]
    auto_thread_emojis = [1477235023970042028, 1477235025723392102]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        
        # Канал идей
        if message.channel.id == self.channel_ids[0]:
            thread = await self.createThread(message, f"Публикация {message.author.display_name}", 1440, self.auto_thread_emojis)
            await database.db.execute(
                """
                INSERT OR REPLACE INTO threads (thread_id, owner_id, message_id, channel_id)
                VALUES (?, ?, ?, ?)
                """,
                (thread.id, message.author.id, message.id, message.channel.id)
            )
            await database.db.commit()
        
        # Канал новостей
        if message.channel.id == self.channel_ids[1]:
            await self.createThread(message, f"{message.content[-5:]} by {message.author.display_name}", 10080, self.auto_thread_emojis)

    async def createThread(self, message, thread_name: str, archive_duration: int, emoji_list: list) -> disnake.Thread:
        author_message = await message.channel.fetch_message(message.id)
        thread = await author_message.create_thread(
            name=thread_name,
            auto_archive_duration=archive_duration
        )
        for emoji in emoji_list:
            await author_message.add_reaction(self.bot.get_emoji(emoji))
        return thread

def setup(bot):
    bot.add_cog(addThreadMessage(bot))
