import disnake
from disnake.ui import View
from disnake.ext import commands
import random
from Cogs.Economy.TerminalCommand import Terminal_Back_Button

phishing_quests = [
    {
        "id": "quest_1",
        "question": "Наталье позвонил человек, представившийся службой безопасности банка, и сообщил о подозрительном переводе. Он попросил назвать код из СМС для отмены операции. Наталья собирается продиктовать код. Ее муж Сергей говорит, что нужно положить трубку и перезвонить в банк по номеру на карте. Кто поступает правильно?",
        "buttons": [
            {"label": "Сергей", "correct": True, "row": 0},
            {"label": "Наталья", "correct": False, "row": 0},
            {"label": "Оба неправы", "correct": False, "row": 0},
            {"label": "Никто", "correct": False, "row": 0}
        ]
    },
    {
        "id": "quest_2",
        "question": "Сергею пришло СМС: Ваша посылка задержана на таможне. Оплатите пошлину 100 рублей по ссылке: cdek-delivery-pay.ru, иначе посылка вернется. Сергей ждет заказ из Китая и хочет перейти по ссылке. Наталья говорит, что ссылка выглядит подозрительно и лучше проверить статус по трек-номеру на официальном сайте. Как следует поступить?",
        "buttons": [
            {"label": "Послушать Наталью", "correct": True, "row": 0},
            {"label": "Оплатить по ссылке", "correct": False, "row": 0},
            {"label": "Просто забыть", "correct": False, "row": 1},
            {"label": "Уточнить по СМС", "correct": False, "row": 1}
        ]
    },
    {
        "id": "quest_3",
        "question": "Наталья работает бухгалтером. Она получает письмо от 'генерального директора' с просьбой срочно перевести крупную сумму новому подрядчику. Адрес отправителя: ceo@c0mpany.com. Наталья начинает оформлять перевод. Сергей замечает странный домен и просит позвонить директору для подтверждения. Кто прав?",
        "buttons": [
            {"label": "Сергей", "correct": True, "row": 0},
            {"label": "Наталья", "correct": False, "row": 0},
            {"label": "Никто", "correct": False, "row": 0},
            {"label": "Оба правы", "correct": False, "row": 0}
        ]
    },
    {
        "id": "quest_4",
        "question": "Сергей сидит в кафе и видит открытую сеть 'Cafe_Free_WiFi'. Он подключается к ней, чтобы зайти в онлайн-банк. Наталья говорит, что без VPN это делать опасно. Сергей отвечает: 'У сайта банка есть HTTPS, мне ничего не угрожает!'. Кто оценивает риски адекватно?",
        "buttons": [
            {"label": "Наталья", "correct": True, "row": 0},
            {"label": "Сергей", "correct": False, "row": 0},
            {"label": "Оба неправы", "correct": False, "row": 0},
            {"label": "Сеть всегда безопасна", "correct": False, "row": 0}
        ]
    },
    {
        "id": "quest_5",
        "question": "В корпоративном мессенджере Наталье пишет 'Администратор ИТ-отдела' и просит прислать пароль от учетки для срочного обновления безопасности. Наталья считает, что нужно помочь. Сергей утверждает, что ИТ-специалисты никогда не просят пароль. Кто прав?",
        "buttons": [
            {"label": "Сергей", "correct": True, "row": 0},
            {"label": "Наталья", "correct": False, "row": 0},
            {"label": "Смотря какая компания", "correct": False, "row": 0},
            {"label": "Оба правы", "correct": False, "row": 0}
        ]
    },
    {
        "id": "quest_6",
        "question": "Сергею в социальной сети пишет старый друг: 'Привет! Срочно одолжи 5000 рублей до завтра, скинь на эту карту...'. Сергей собирается перевести деньги. Наталья советует сначала позвонить другу по телефону. Как следует поступить?",
        "buttons": [
            {"label": "Позвонить другу", "correct": True, "row": 0},
            {"label": "Быстро перевести", "correct": False, "row": 0},
            {"label": "Перевести половину", "correct": False, "row": 1},
            {"label": "Спросить в ответном СМС", "correct": False, "row": 1}
        ]
    },
    {
        "id": "quest_7",
        "question": "На личную почту Натальи приходит письмо от 'Налоговой службы' с архивом doc_nalog.zip, который требуют открыть в течение 24 часов. Наталья хочет открыть файл. Сергей говорит, что нужно удалить письмо и проверить налоги через Госуслуги. Кто прав?",
        "buttons": [
            {"label": "Сергей", "correct": True, "row": 0},
            {"label": "Наталья", "correct": False, "row": 0},
            {"label": "Антивирус защитит", "correct": False, "row": 0},
            {"label": "Оба неправы", "correct": False, "row": 0}
        ]
    },
    {
        "id": "quest_8",
        "question": "Наталья зашла на сайт с рецептами. На весь экран появляется красное окно: 'Ваш ПК заражен 5 вирусами! Нажмите здесь, чтобы скачать утилиту очистки!'. Наталья тянется нажать 'Скачать'. Сергей говорит просто закрыть вкладку браузера. Как поступить?",
        "buttons": [
            {"label": "Закрыть вкладку", "correct": True, "row": 0},
            {"label": "Скачать утилиту", "correct": False, "row": 0},
            {"label": "Выдернуть шнур ПК", "correct": False, "row": 1},
            {"label": "Ввести номер телефона", "correct": False, "row": 1}
        ]
    },
    {
        "id": "quest_9",
        "question": "Сергею приходит письмо: 'Наталья поделилась с вами документом'. Ссылка открывает страницу входа, но URL-адрес выглядит как g00gle-docs-login.com. Сергей не обращает внимания и вводит пароль. В чем его главная ошибка?",
        "buttons": [
            {"label": "Не проверил URL-адрес", "correct": True, "row": 0},
            {"label": "Не включил VPN", "correct": False, "row": 0},
            {"label": "Ввел пароль от основы", "correct": False, "row": 1},
            {"label": "Ошибки нет", "correct": False, "row": 1}
        ]
    },
    {
        "id": "quest_10",
        "question": "Наталья нашла на улице красивую флешку и хочет вставить ее в рабочий ноутбук, чтобы найти владельца. Сергей предупреждает, что это может быть атака (Drop attack), и флешку вставлять нельзя. Как лучше поступить?",
        "buttons": [
            {"label": "Сдать в ИБ / Выбросить", "correct": True, "row": 0},
            {"label": "Вставить и проверить", "correct": False, "row": 0},
            {"label": "Проверить антивирусом", "correct": False, "row": 1},
            {"label": "Вставить в ПК с Linux", "correct": False, "row": 1}
        ]
    }
]

class PhishingGameLogic(disnake.ui.View):
    def __init__(self, terminal, game_emoji):
        super().__init__(timeout=60)
        self.terminal = terminal
        self.game_emoji = game_emoji
        self.quest = random.choice(phishing_quests)

        for index, answer in enumerate(self.quest["buttons"]):
            button = disnake.ui.Button(
               label=answer["label"],
               style=disnake.ButtonStyle.secondary,
               custom_id="correct" if answer["correct"] else f"wrong_{index}" 
            )
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, body: disnake.MessageInteraction):
        self.clear_items()
        self.add_item(Terminal_Back_Button(self.terminal, self.game_emoji))

        if body.component.custom_id == "correct":
            return await body.response.edit_message(f"# <a:trophy:{self.game_emoji['Regex Game']}> Ты сдержал злоумышленника!\n- Ты ` ответил ` правильно и ` спас ` кого-то", view=self)
        await body.response.edit_message(f"# <a:denied:{self.game_emoji['Brute-Force Attack']}> Кто-то пострадал..\n- Ты ` ответил ` неправильно, мудак", view=self)

class Phishing(disnake.ui.Button):
    def __init__(self, terminal, game_emoji):
        self.terminal = terminal
        self.game_emoji = game_emoji

        super().__init__(
            label="Phishing Finder",
            style=disnake.ButtonStyle.danger,
            emoji=disnake.PartialEmoji(
               name="Phishing",
               id=game_emoji["Phishing Game"] 
            )
        )
    async def callback(self, body: disnake.MessageInteraction):
        view = PhishingGameLogic(self.terminal, self.game_emoji)
        await body.response.edit_message(
           f"# <a:phishing:{self.game_emoji['Phishing Game']}> #НЕТФИШИНГУ\n" 
           f"- {view.quest['question']}\n> Выбирай подходящие варианты",
           view=view 
        )
