import disnake
from disnake.ext import commands, tasks
import aiohttp
import random

class NewsParser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = aiohttp.ClientSession()
        self.parser.start()
        self.auto_message_emojis = [1477235023970042028, 1477235025723392102]


    @tasks.loop(hours=24)
    async def parser(self):
        async with self.client.get("https://newsapi.org/v2/everything?q=AI OR programming OR software&language=ru&from=2026-04-01&sortBy=publishedAt&apiKey=66e1fa12c72847cd9226a1f590efd367") as response:
            data = await response.json()
        article = random.choice(data["articles"])
        embed = disnake.Embed(
            title="",
            description=
            f"# {self.bot.get_emoji(1477235040084557848)} Новостная лента\n"
            f"- {article['title']}\n"
            f"> {article['description']}\n"
            f"\nСтатья: ||{article['url']}||",
            color=0x7e57ff
        )
        image_url = article['urlToImage']
        embed.set_footer(text=f"{article['publishedAt'][:10]}")
        embed.set_image(url=image_url) if image_url and image_url.startswith(("https://", "http://")) else None

        channel = self.bot.get_channel(1476962060092051547)
        message = await channel.send(embed=embed)
        for emoji in self.auto_message_emojis:
            await message.add_reaction(self.bot.get_emoji(emoji))

def setup(bot):
    bot.add_cog(NewsParser(bot))
