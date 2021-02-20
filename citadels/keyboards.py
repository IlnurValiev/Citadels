import telebot

CHARACTERS = [
        '1️⃣ '+'Ассасин ' + chr(0x1F977),
        '2️⃣ '+'Вор ' + chr(0x1F9B9),
        '3️⃣ '+'Чародей ' + chr(0x1F9D9),
        '4️⃣ '+'Король ' +  chr(0x1F934) ,
        '5️⃣ '+'Епископ '  + chr(0x1F473),
        '6️⃣ '+'Купец '  + chr(0x1F935),
        '7️⃣ '+'Зодчий '  + chr(0x1F477),
        '8️⃣ '+'Кондотьер '  +  chr(0x1F482),
        ]

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row("Играть 🎮")
keyboard1.row("Правила 📖")
keyboard1.row("Выход")

keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Скачать pdf 📜')
keyboard2.row('Видео 🎞')
keyboard2.row('Персонажи 🎭')
keyboard2.row('Кварталы 🏛')
keyboard2.row('Главное меню')

keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row('Дворянские 🟡')
keyboard3.row('Торговые 🟢')
keyboard3.row('Церковные 🔵')
keyboard3.row('Воинские 🔴')
keyboard3.row('Особые 🟣')
keyboard3.row('Правила')

keyboard4 = telebot.types.ReplyKeyboardMarkup(True)
keyboard4.row(CHARACTERS[0], CHARACTERS[1])
keyboard4.row(CHARACTERS[2], CHARACTERS[3])
keyboard4.row(CHARACTERS[4], CHARACTERS[5])
keyboard4.row(CHARACTERS[6], CHARACTERS[7])
keyboard4.row('Правила')

keyboard5 = telebot.types.ReplyKeyboardMarkup(True)
keyboard5.row('Игроки 👥')
keyboard5.row('Персонажи 🎭')
keyboard5.row('Старт 🙋‍♂️')
keyboard5.row('Выход')

keyboard6 = telebot.types.ReplyKeyboardMarkup(True)
keyboard6.row('Игроки 👥')
keyboard6.row('Персонажи 🎭')
keyboard6.row('Старт 🙋‍♂️')
keyboard6.row('Отмена ❌')
keyboard6.row('Выход')

keyboard7 = telebot.types.ReplyKeyboardMarkup(True)
keyboard7.row('Игроки 👥')
keyboard7.row('Персонажи 🎭')
keyboard7.row('Выход')
