import disnake
import asyncio
from disnake.ext import commands

class StartTerminal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_emoji = {
            "Terminal_Process_Open": 1490239885653577829,
            "Terminal_Main_Window": 1490239953970663527
            }

    @commands.slash_command(description="Открывает терминал", guild_ids=[1466509350100013226])
    async def terminal(self, body: disnake.ApplicationCommandInteraction):
        await body.response.send_message(
                f"# {self.bot.get_emoji(self.game_emoji['Terminal_Process_Open'])} Открываем...",
                ephemeral=True
                )
        await asyncio.sleep(2)
        await body.edit_original_response(
                f"# {self.bot.get_emoji(self.game_emoji['Terminal_Main_Window'])} Привет, {body.author.mention}!\n"
                f"- Терминал: ` открыт ` (/home/**{body.author.name}**)\n"
                "- Сторона: ` RedTeam `"
                "> Управляйте терминалом через ` GUI `",
                allowed_mentions=disnake.AllowedMentions.none()
                )

def setup(bot):
    bot.add_cog(StartTerminal(bot))
