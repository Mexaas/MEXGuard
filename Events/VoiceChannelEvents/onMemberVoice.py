from disnake.ext import commands

class CustomVoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.add_channel = 1489602321859215520

    @commands.Cog.listener()
    async def on_voice_state_update(
            self, member, before, after
    ):
        if before.channel:
            if "Комната" in before.channel.name:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
        if after.channel and after.channel.id == self.add_channel:
            overwrites = {
                member.guild.default_role: disnake.PermissionOverwrite(connect=True),
                member: disnake.PermissionOverwrite
                    manage_channels=True,
                    move_members=True,
                    mute_members=True,
                    priority_speaker=True
                )
            }
            new_channel = await member.guild.create_voice_channel(
                    name=f"Комната {member.display_name}",
                    category=after.channel.category,
                    overwrites=overwrites
                    )
            await member.move_to(new_channel)

def setup(bot):
    bot.add_cog(CustomVoiceChannel(bot))
        
