import disnake
from disnake.ext import commands, tasks
import aiohttp
import random

class NewsParser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parser.start()

    @tasks.loop(hours=12)
    async def parser(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://newsapi.org/v2/everything?q=AI OR programming OR software&language=ru&from=2026-02-07&sortBy=publishedAt&apiKey=8cbb420939284f91abd0df532509e90b") as response:
                data = await response.json()
        article = random.choice(data["articles"])
        embed = disnake.Embed(
            title="",
            description=
            f"# {self.bot.get_emoji(1477235040084557848)} Новостная лента\n"
            f"- {article['title'].capitalize()}\n"
            f"> {article['description']}\n" 
            f"\nСтатья: ||{article['url']}||",
            color=0x7e57ff
        )
        image_url = article['urlToImage']
        embed.set_footer(text=f"{article['publishedAt'][:10]}")
        embed.set_image(url=image_url) if image_url and image_url.startswith(("https://", "http://")) else None

        channel = self.bot.get_channel(1476962060092051547)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(NewsParser(bot))