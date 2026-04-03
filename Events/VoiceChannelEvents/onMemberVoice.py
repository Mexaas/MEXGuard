import disnake
from disnake.ext import commands

class CustomVoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.add_channel = 1477280288265474139

    @commands.Cog.listener()
    async def on_voice_state_update(
            self, member, before, after
    ):
        if (before.channel is not None and member.name.lower() in before.channel.name.lower()) and (after.channel is None or after.channel is not None):

            await before.channel.delete()
        category = member.guild.get_channel(self.add_channel)
        if ((before.channel is None or before.channel is not None) and after.channel == category):
            new_channel = await member.guild.create_voice_channel(
                    name=f"Комната {member.name}",
                    category=after.channel.category
                    )
            await member.move_to(new_channel)

def setup(bot):
    bot.add_cog(CustomVoiceChannel(bot))
        
