from disnake.ext import commands
import disnake
from pathlib import Path
from Database.database import db

class DropDownView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.data = {}
        self.cache = {}
        self.message = None
        self.emojis = [1477235020740690023]
        welcome_button = disnake.ui.Button(
            label="Поприветствовать",
            style=disnake.ButtonStyle.secondary,
            custom_id="welcome_button",
            emoji="💜"
        )
        welcome_button.callback = self.welcome_callback
        self.add_item(welcome_button)
    
    async def on_timeout(self):
        self.cache.clear()
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    async def welcome_callback(self, body: disnake.MessageInteraction):
        if body.message.id in self.data:
            newbie_id = self.data[body.message.id]
            newbie_role = (await body.guild.fetch_member(newbie_id)).get_role(1476451132560773161)
            newbie_user = await body.guild.fetch_member(newbie_id)
            if newbie_role:
                if body.author.id == newbie_id:
                    await body.response.send_message(
                        f"# :x: Ошибка!\n"
                        f"- Вы не можете поприветствовать ` самого ` себя!",
                        ephemeral=True,
                        delete_after=20
                    )
                    return
                if body.message.id in self.cache.get(body.author.id, set()):
                    await body.response.send_message(
                        f"# :x: Ошибка!\n"
                        f"- Вы уже поприветствовали ` данного ` пользователя!",
                        ephemeral=True,
                        delete_after=20
                    )
                    return
                await body.response.send_message(
                    f"# {await body.guild.fetch_emoji(self.emojis[0])} Система приветствий\n"
                    f"- {newbie_user.mention}, вас поприветствовал {body.user.mention}!",
                    delete_after=20
                )
                self.cache.setdefault(body.author.id, set()).add(body.message.id)
                return
            await body.response.send_message(f"# :x: Ошибка!\n- Пользователь еще не ` прошёл капчу `!", ephemeral=True, delete_after=10)

class FirstMemberJoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_type = {
            "member_join": "Content/HelloMember_Image.png"
        }
    def get_image(self, value: str) -> disnake.File:
        return disnake.File(self.image_type[value], Path(self.image_type[value]).name)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot: return
        channel = self.bot.get_channel(1477022604778012765)
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, join_value) VALUES (?, ?)",
            (member.id, 1)
        )
        await db.commit()

        view = DropDownView()
        message = await channel.send(
            f"# {self.bot.get_emoji(1477235374127452160)} Привет, {member.mention}!\n"
            f"- Очень ` рады ` видеть тебя на сервере\n"
            f"> Для подробной информации советуем воспользоваться\n"
            f"> специальным меню навигации по серверу, просто введи ` /menu `\n",
            file=self.get_image("member_join"),
            view=view
        )
        view.message = message
        view.data[message.id] = member.id

def setup(bot):
    bot.add_cog(FirstMemberJoinEvent(bot))