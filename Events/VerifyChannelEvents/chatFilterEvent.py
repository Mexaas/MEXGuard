import disnake
from disnake.ext import commands

class MessageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    allowed_messages = ["/captcha", "/verify"]
    channel_ids = [1476542488528425096]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.channel.id == self.channel_ids[0]:
            if message.content.lower() not in self.allowed_messages:
                await message.channel.send(
                    f"""
                    # :x: Ошибка
                    - {message.author.mention}, кажется здесь нет связи...
                    
                    > Может стоит попробовать ` /captcha `?
                    > ходят, что здесь практически ничего недоступно
                    """,
                    delete_after=4
                )
                await message.delete()
            else: return
        else: return


def setup(bot):
    bot.add_cog(MessageFilter(bot))