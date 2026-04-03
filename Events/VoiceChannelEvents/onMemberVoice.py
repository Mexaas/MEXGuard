from disnake.ext import commands

class CustomVoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.add_channel = 1477280288265474139

    @commands.Cog.listener()
    async def on_voice_state_update(
            self, member, before, after
    ):
        if not before.channel.members:
            await before.channel.delete()

        if before.channel and member.name.lower() in before.channel.name.lower():
            if not before.channel.members:
                await before.channel.delete()
        if after.channel and after.channel.id == self.add_channel:
            new_channel = await member.guild.create_voice_channel(
                    name=f"Комната {member.display_name}",
                    category=after.channel.category
                    )
            await member.move_to(new_channel)

def setup(bot):
    bot.add_cog(CustomVoiceChannel(bot))
        
