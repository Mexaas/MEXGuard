import os
import disnake
from disnake.ext import commands
from Database import database

intents = disnake.Intents().all()
bot = commands.InteractionBot(
    intents=intents,
    activity=disnake.CustomActivity(name="🌸 /menu")
)

class Bot(commands.InteractionBot):
    async def setup_hook(self):
        for folder in ("Cogs", "Events"):
            for file in os.listdir(folder):
                path = f"{folder}/{file}"
                if os.path.isdir(path):
                    self.load_extensions(path)

        await database.init()
        await database.db.execute("PRAGMA journal_mode=WAL;")
        await database.db.commit()

@bot.event
async def on_ready():
    print(
        f"""
        #######################
        #                     #
        # 🚀 {bot.user}   #
        # 🔓 Bot is starting  #
        #                     #
        #######################
        """
    )

bot.run(os.getenv("DISCORD_TOKEN"))
