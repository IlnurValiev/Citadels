import telebot
import random as ran
import time
import quarters as q
import keyboards as key

TG_TOKEN = ''
bot = telebot.TeleBot(TG_TOKEN)

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

remove_keyboard = telebot.types.ReplyKeyboardRemove(True)

players_id = []

players_names = []

start_voters = []

game_Is_Started = False

ACTIVE_CHARS = CHARACTERS

OPENED_CARDS = [

]

class Player():
    def __init__(self):
        self.id = ''
        self.chars = []
        self.quarts = []
        self.b_quarts = []
        self.coins = ''
    
    def __str__(self):
        return ('Кварталы на руках:\n{}\nПостроенные кварталы:\n{}'+'Монеты:'+self.coins*'🏅').format('\n'.join(map(str, self.quarts)), '\n'.join(map(str, self.b_quarts)))

    def add_quart(self, quart):
        self.quarts.append(quart)

player1  = Player()
player2  = Player()
player3  = Player()
player4  = Player()
player5  = Player()
player6  = Player()
player7  = Player()

Players = [player1, player2, player3, player4, player5, player6, player7]

choising = True

draft_index = 0

rounds_start = True 

draft_start = True

keyboard8 = telebot.types.ReplyKeyboardMarkup(True)

CLOSED_CARD = ''

waiters_id = []  

waiters_names = []

playing = False

games_start = True

def reload_keyboard():
    global keyboard8
    
    keyboard8 = telebot.types.ReplyKeyboardMarkup(True)

    keyboard8.row('Игроки 👥')
    keyboard8.row('Персонажи 🎭')
    for charac in ACTIVE_CHARS:
        keyboard8.row(charac)
    keyboard8.row('Выход')

def draft3_7():
    
    global ACTIVE_CHARS
    global OPENED_CARDS

    if len(players_id) != 7 and (len(players_id) != 3):
            
        CLOSED_CARD = ran.choice(ACTIVE_CHARS)
        ACTIVE_CHARS.remove(CLOSED_CARD)
            
        for i in range(0,6-len(players_id)):
            rand_card = ran.choice(ACTIVE_CHARS)

            OPENED_CARDS.append(rand_card)
            ACTIVE_CHARS.remove(rand_card)
    else:
        CLOSED_CARD = ran.choice(ACTIVE_CHARS)
        ACTIVE_CHARS.remove(CLOSED_CARD)


    OPENED_CARDS.sort()
    ACTIVE_CHARS.sort()

def send_to_all_membs(message, keyboard = ''):
    if keyboard == '':
        for player in players_id + waiters_id:
            bot.send_message(player, message)
    else:
        for player in players_id + waiters_id:
            bot.send_message(player, message, reply_markup = keyboard)

def your_turn():
    global draft_start
    global ACTIVE_CHARS

    if draft_index == 6:
        ACTIVE_CHARS.append(CLOSED_CARD)

    if draft_start and (draft_index < len(players_id)):
        bot.send_message(players_id[draft_index], 'Ваша очередь выбрать персонажа.\nНажмите на кнопку, чтобы это сделать.\nЧтобы получить информацию о персонаже, введите его название', reply_markup = keyboard8)

        for i in range(len(players_id)):
            if i != draft_index:
                bot.send_message(players_id[i], players_names[draft_index] + ' выбирает персонажа', reply_markup = key.keyboard7)

        for player in waiters_id:
            bot.send_message(player, players_names[draft_index] + ' выбирает персонажа', reply_markup = key.keyboard7)

        draft_start = False

def draft_quarts():

    for i in range(0, len(players_id)):
        Players[i].id = players_id[i]
        Players[i].coins = 2

        for k in range(0,4):
            rand_quart = ran.choice(q.quarts)
            Players[i].add_quart(rand_quart)
            q.quarts.remove(rand_quart)

        bot.send_message(Players[i].id, Players[i])

def char_chosen(message, chat_id):
        
        message = str(message)

        global draft_start
        global draft_index
        global ACTIVE_CHARS
        global playing

        if (('1️⃣ '+'ассасин ' + chr(0x1F977) == message.lower()) or
                ('2️⃣ '+'вор ' + chr(0x1F9B9)== message.lower()) or
                ('3️⃣ '+'чародей ' + chr(0x1F9D9)== message.lower()) or
                ('4️⃣ '+'король ' +  chr(0x1F934) == message.lower()) or
                ('5️⃣ '+'епископ '  + chr(0x1F473) == message.lower()) or
                ('6️⃣ '+'купец '  + chr(0x1F935) == message.lower()) or
                ('7️⃣ '+'зодчий '  + chr(0x1F477) == message.lower()) or
                ('8️⃣ '+'кондотьер '  +  chr(0x1F482) == message.lower()) and
                (chat_id == players_id[draft_index]) and 
                (message in ACTIVE_CHARS)):

            bot.send_message(players_id[draft_index], 'Отлично!\nВ этом раунде вы ' + message, reply_markup = key.keyboard7)

            Players[draft_index].chars.append(message)
                       
            ACTIVE_CHARS.remove(message)
            ACTIVE_CHARS.sort()
                    
            draft_index = (draft_index + 1)%len(players_id)

            if len(ACTIVE_CHARS) == 1:
                draft_start = False
                ACTIVE_CHARS.clear()
                playing = True
            else:
                draft_start = True

            reload_keyboard()

def draft2():
    global ACTIVE_CHARS
    closed = ran.choice(ACTIVE_CHARS)
    ACTIVE_CHARS.remove(closed)

@bot.message_handler(commands=['start'])
def start(message):
    with open('main.jpg', 'rb') as ph:
        photo = ph.read()
    bot.send_photo(message.chat.id, photo, caption = '''Добро пожаловать в "Цитадели"!

Игра о средневековых городах, благородстве и интригах.
    ''', reply_markup = key.keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
  
  global ACTIVE_CHARS
  global OPENED_CARDS
  global CLOSED_CARD
  global players_id
  global waiters_id
  global players_names
  global start_voters
  global game_Is_Started
  global draft_index
  global choising
  global rounds_start
  global draft_start
  global player1
  global player2
  global keyboard8
  global waiters_names
  global playing
  global games_start

  if((game_Is_Started and
     (message.chat.id not in players_id+waiters_id)) or
    (not game_Is_Started )):

    if ((message.text.lower() == 'выход') and 
       (message.chat.id in players_id+waiters_id)):
        bot.send_message(message.chat.id, 'Вы вышли из игры', reply_markup = key.keyboard1)
        
        if message.chat.id in players_id:
            players_names.remove(players_names[players_id.index(message.chat.id)])
            players_id.remove(message.chat.id)

        if message.chat.id in waiters_id:
            waiters_names.remove(waiters_names[waiters_id.index(message.chat.id)])

        for i in range(0, len(players_id)):
                if(len(players_id) > 1):
                    bot.send_message(players_id[i], message.from_user.first_name + ' вышел из игры', reply_markup = key.keyboard5)
                else:
                    bot.send_message(players_id[i], message.from_user.first_name + ' вышел из игры', reply_markup = key.keyboard7)
        
        if message.chat.id in start_voters:
            start_voters.remove(message.chat.id)

    for i in range(0, len(players_id)):
        if (players_id[i] != message.chat.id and 
           (message.chat.id in players_id) and 
           (message.text.lower() != ('старт 🙋‍♂️')) and
           (message.text.lower() != ('старт')) and
           (message.text.lower() != ('персонажи 🎭')) and
           (message.text.lower() != ('персонажи')) and 
           (message.text.lower() != ('игроки 👥')) and
           (message.text.lower() != ('отмена ❌')) and
           (message.text.lower() != ('отмена')) and
           (message.text.lower() != ('выход')) and
           (message.text.lower() != ('игроки')) and
           ('ассасин' != message.text.lower()) and
           ('вор' != message.text.lower()) and
           ('чародей' != message.text.lower()) and
           ('король' != message.text.lower()) and
           ('епископ' != message.text.lower()) and
           ('купец' != message.text.lower()) and
           ('зодчий' != message.text.lower()) and
           ('кондотьер' != message.text.lower())):
            bot.send_message(players_id[i], message.from_user.first_name + ': '+ message.text)

    if 'играть' in message.text.lower() and (message.chat.id not in players_id + waiters_id):

        if len(players_id + waiters_id) == 7:
            bot.send_message(message.chat.id, 'К сожалению, вы не можете присоединиться к игре: комната заполнена, участвовать могут не более 7 человек. Дождитесь выхода одного из игроков.')
        else:
            if game_Is_Started:
                waiters_id.append(message.chat.id)
                waiters_names.append(message.from_user.first_name)
                bot.send_message(message.chat.id,'Игра уже начата. Дождитесь ее окончания и можете присоединиться.')
            else:   
                players_id.append(message.chat.id)
                players_names.append(message.from_user.first_name)        
            
                if(len(players_id) > 1):
                    bot.send_message(message.chat.id, 'Вы в игре!\n'+
                'Могут участвовать от 2 до 7 человек. Чтобы начать, введите "старт".'+
                ' Как только проголосуют все, игра начнется. \n'+
                'Список игроков: ' + ', '.join(map(str, players_names)), 
                reply_markup = key.keyboard5)
                else: bot.send_message(message.chat.id, 'Вы в игре!\n'+
                'Могут участвовать от 2 до 7 человек. Чтобы начать, введите "старт".'+
                ' Как только проголосуют все, игра начнется. \n'+
                'Список игроков: ' + ', '.join(map(str, players_names)), 
                reply_markup = key.keyboard7)
                
            for player in (players_id + waiters_id):
                if player != message.chat.id:
                    if message.chat.id in waiters_id:
                        bot.send_message(player, message.from_user.first_name + ' присоединился(ась) к игре')
                    else:
                        bot.send_message(player, message.from_user.first_name + ' присоединился(ась) к игре', reply_markup = key.keyboard5)

    
    if((message.text.lower() == 'старт' or
      message.text.lower() == 'старт 🙋‍♂️') and
      (message.chat.id in players_id) and
      (message.chat.id not in start_voters)):

        start_voters.append(message.chat.id)

        if(len(players_id) <= 1):
          bot.send_message(message.chat.id, 'Недостаточно игроков для начала игры.')
          start_voters.remove(message.chat.id)
        else:    
          for i in range(0, len(players_id)):
            if(message.chat.id != players_id[i]):
                bot.send_message(players_id[i], message.from_user.first_name +
            ' проголосовал(а) за начало игры.\n\n' +
            'Всего голосов: ' +
            str(len(start_voters))+'/'+str(len(players_id)))
            else:
                bot.send_message(players_id[i], 'Вы проголосовали. Чтобы отменить свой голос, введите "отмена".\n\n' +
            'Всего голосов: ' +
            str(len(start_voters))+'/'+str(len(players_id)),
             reply_markup = key.keyboard6)
    elif((message.text.lower() == 'старт' or
         message.text.lower() == 'старт 🙋‍♂️') and
         (message.chat.id in players_id) and
         (message.chat.id in start_voters)):
        bot.send_message(message.chat.id,'Вы уже проголосовали. Для отмены голоса введите "отмена"')

    if (len(start_voters) == len(players_id) and (message.chat.id in players_id)):
        game_Is_Started = True
        start_voters.clear()
        for i in range(0, len(players_id)):
            bot.send_message(players_id[i], 'Проголосовали все!\nИгра началась!', reply_markup = key.keyboard7)

    if(((message.text.lower() == 'отмена') or
       (message.text.lower() == 'отмена ❌')) and
       (message.chat.id in players_id) and
       (message.chat.id in start_voters) and
       not game_Is_Started):
        start_voters.remove(message.chat.id)

        for i in range(0, len(players_id)):
            if(message.chat.id != players_id[i]):
                bot.send_message(players_id[i], message.from_user.first_name +
                ' отменил(а) свой голос.\n\n' +
                'Всего голосов: ' +
            str(len(start_voters))+'/'+str(len(players_id)))
            else:
                bot.send_message(players_id[i], 'Ваш голос отменен.\n\n'+
                'Всего прогосовавших: ' +
            str(len(start_voters))+'/'+str(len(players_id)),
             reply_markup = key.keyboard5)

    elif(((message.text.lower() == 'отмена') or
       (message.text.lower() == 'отмена ❌')) and
       (message.chat.id in players_id) and
       (message.chat.id not in start_voters)):
        bot.send_message(message.chat.id,'Вы не проголосовали. Нажмите "старт" чтобы это сделать.')

    if ('игроки' == message.text.lower() or 
        'игроки 👥' == message.text.lower()):
        bot.send_message(message.chat.id, 'Список игроков:\n'+'\n'.join(map(str, players_names)))

    if 'правила' in message.text.lower() and (message.chat.id not in players_id):
        bot.send_message(message.chat.id, 'Вы можете скачать правила в формате pdf, посмотреть видео, а также открыть список персонажей или кварталов',
          reply_markup = key.keyboard2)
    
    if ('меню' in message.text.lower()) and message.chat.id not in players_id:
       bot.send_message(message.chat.id, '''Главное меню.\n\nВы можете начать играть или ознакомиться с правилами.
    ''', reply_markup = key.keyboard1)

    if 'скачать' in message.text.lower() and message.chat.id not in players_id :
        bot.send_message(message.chat.id, 'https://drive.google.com/file/d/1hX99Yhy1OFS5dEwxlpTBEaq5wRfu56vd/view?usp=sharing')
    
    if 'видео' in message.text.lower() and message.chat.id not in players_id:
         bot.send_message(message.chat.id, 'http://bit.ly/2msLOlA')
    
    if "персонажи" in message.text.lower() and message.chat.id not in players_id:
        bot.send_message(message.chat.id,'Очередь хода | персонаж\n\n' +
        '\n'.join(map(str, CHARACTERS)),reply_markup = key.keyboard4)
    elif ("персонажи" == message.text.lower() or
          "персонажи 🎭" == message.text.lower()):
        bot.send_message(message.chat.id,'Очередь хода | персонаж\n\n'+ 
        '\n'.join(map(str, CHARACTERS))+'\n\nЧтобы получить информацию о персонаже, введите его название')

    if 'кварталы' in message.text.lower() and message.chat.id not in players_id:
        bot.send_message(message.chat.id, 
                '''Некоторые персонажи получают по одной монетке за каждый квартал своего типа:

Король 🤴  – дворянский 🟡

Епископ 👳 – церковный 🔵

Купец 🤵 – торговый 🟢

Кондотьер 💂 – военный  🔴

Особые кварталы 🟣 дают Вам различные бонусы'''
                , reply_markup = key.keyboard3)
   
    if ('ассасин' == message.text.lower()  or
         message.text.lower() == CHARACTERS[0].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[0] + '''\nМожете назвать другого персонажа, которого
хотите убить. Убитый ничем не выдает себя и обязан промолчать когда настанет его ход. Ход убитого персонажа пропускается.''' )

    if ('вор' == message.text.lower() or
         message.text.lower() == CHARACTERS[1].lower()):
        bot.send_message(message.chat.id,
        CHARACTERS[1] + '''\nМожете назвать другого персонажа, которого
хотите обворовать. Когда его вызывают, заберите у его владельца всё золото. Воровать
у ассасина или у жертвы ассасина нельзя''')

    if ('чародей' == message.text.lower()  or
         message.text.lower() == CHARACTERS[2].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[2] + '''\nВ любой момент хода можете выполнить
одно из двух действий: обменять все свои карты с руки (не в городе)
на карты с руки другого игрока; вы вправе
произвести такой обмен, даже если карт
у вас на руке нет, — просто заберите карты
у соперника;
вернуть сколько угодно карт с руки под
колоду кварталов и взять из неё столько же
новых карт кварталов.'''
        )

    if ('король' == message.text.lower() or
         message.text.lower() == CHARACTERS[3].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[3] + '''\nПолучите один золотой за каждый дворянский (жёлтый) квартал в вашем городе. В свой
ход вы должны взять корону. В следующем ра-
унде первым будете выбирать персонажа. Если
короля никто не выбрал, корона остаётся у предыдущего владельца. Если король выбран, но убит, его владелец пропускает ход, как и всякий другой персонаж, но в конце раунда получает или сохраняет корону как наследник престола.'''
        )

    if ('епископ' == message.text.lower() or
         message.text.lower() == CHARACTERS[4].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[4] + '''\nПолучите один золотой за каждый церковный (синий) квартал в вашем городе.
В этом раунде кондотьер не может разрушить ваши кварталы. Но если вы убиты, то может.''')

    if ('купец' == message.text.lower() or
         message.text.lower() == CHARACTERS[5].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[5] + '''\nПолучите один золотой за каждый торговый (зелёный) квартал в вашем городе. Вы получаете один дополнительный золотой. Это свойство действует независимо от того, какие ресурсы вы собрали в этом ходу.'''
        )

    if ('зодчий' == message.text.lower() or
         message.text.lower() == CHARACTERS[6].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[6] + '''\nВы получаете две дополнительные карты.
Это свойство действует независимо от того,
какие ресурсы вы собрали в этом ходу. В свой
ход можете построить три квартала или
меньше.''')

    if  (message.text.lower() == ('кондотьер') or
         message.text.lower() == CHARACTERS[7].lower()):
        bot.send_message(message.chat.id, 
        CHARACTERS[7] + '''\nПолучите один золотой за каждый воинский
(красный) квартал в вашем городе. Вы можете
разрушить один квартал в любом городе
(в том числе в своём) по вашему выбору, заплатив на один золотой меньше стоимости
квартала. Квартал ценой в 1 золотой вы сносите бесплатно, на разрушение квартала ценой в 2 золотых уйдёт 1 монета, квартал ценой
в 5 золотых потребует 4 монеты и т. п. Вы не
можете сносить кварталы в достроенном городе. Уничтоженные кварталы сбрасываются
в закрытую под низ колоды кварталов.''')
    
    if (message.chat.id in players_id):
        if(players_names[players_id.index(message.chat.id)] != message.from_user.first_name):
            players_names[players_id.index(message.chat.id)] = message.from_user.first_name
    
  if game_Is_Started and (message.chat.id in players_id+waiters_id):

        if ((message.text.lower() == 'выход') and 
            (message.chat.id in players_id+waiters_id)):
            bot.send_message(message.chat.id, 'Вы вышли из игры', reply_markup = key.keyboard1)

            if message.chat.id in players_id:        
                players_names.remove(players_names[players_id.index(message.chat.id)])
                players_id.remove(message.chat.id)

                
            else:
                waiters_id.remove(message.chat.id)

            for player in players_id+waiters_id:

                bot.send_message(player, message.from_user.first_name + ' вышел из игры', reply_markup = key.keyboard7)
                                
            if(len(players_id) <= 1):
                send_to_all_membs ('Игра завершена из-за нехватки игроков', key.keyboard7)
                game_Is_Started = False
                choising = True
                ACTIVE_CHARS = [
                '1️⃣ '+'Ассасин ' + chr(0x1F977),
                '2️⃣ '+'Вор ' + chr(0x1F9B9),
                '3️⃣ '+'Чародей ' + chr(0x1F9D9),
                '4️⃣ '+'Король ' +  chr(0x1F934) ,
                '5️⃣ '+'Епископ '  + chr(0x1F473),
                '6️⃣ '+'Купец '  + chr(0x1F935),
                '7️⃣ '+'Зодчий '  + chr(0x1F477),
                '8️⃣ '+'Кондотьер '  +  chr(0x1F482),
                ]
                
                CLOSED_CARD = ''
                OPENED_CARDS.clear()
                draft_index = 0
                rounds_start = True 
                draft_start = True
                playing = False
                games_start = True

                for player in Players:
                    player.id = ''
                    player.char = ''
                    player.quarts = []
                    player.b_quarts = []
                    player.coins = ''

                if message.chat.id in start_voters:
                    start_voters.remove(message.chat.id)

        for player in players_id+waiters_id:
            if (player != message.chat.id and  
                (message.text.lower() != ('старт 🙋‍♂️')) and
                (message.text.lower() != ('старт')) and
                (message.text.lower() != ('персонажи 🎭')) and
                (message.text.lower() != ('персонажи')) and 
                (message.text.lower() != ('игроки 👥')) and
                (message.text.lower() != ('выход')) and
                (message.text.lower() != ('игроки')) and
                (message.text.lower() != ('играть')) and
                ('ассасин' != message.text.lower()) and
                ('вор' != message.text.lower()) and
                ('чародей' != message.text.lower()) and
                ('король' != message.text.lower()) and
                ('епископ' != message.text.lower()) and
                ('купец' != message.text.lower()) and
                ('зодчий' != message.text.lower()) and
                ('кондотьер' != message.text.lower()) and
                ('1️⃣ '+'ассасин ' + chr(0x1F977) != message.text.lower()) and
                ('2️⃣ '+'вор ' + chr(0x1F9B9)!= message.text.lower()) and
                ('3️⃣ '+'чародей ' + chr(0x1F9D9)!= message.text.lower()) and
                ('4️⃣ '+'король ' +  chr(0x1F934)!= message.text.lower()) and
                ('5️⃣ '+'епископ '  + chr(0x1F473)!= message.text.lower()) and
                ('6️⃣ '+'купец '  + chr(0x1F935)!= message.text.lower()) and
                ('7️⃣ '+'зодчий '  + chr(0x1F477)!= message.text.lower()) and
                ('8️⃣ '+'кондотьер '  +  chr(0x1F482))!= message.text.lower()):
                bot.send_message(player, message.from_user.first_name + ': ' + message.text)
                
        if ('игроки' == message.text.lower() or 
            'игроки 👥' == message.text.lower()):
            bot.send_message(message.chat.id, 'Список игроков:\n'+'\n'.join(map(str, players_names)) + '\nОжидающие:\n' + '\n'.join(map(str, waiters_id)))

        if ("персонажи" == message.text.lower() or
            "персонажи 🎭" == message.text.lower()):
            bot.send_message(message.chat.id,'Очередь хода | персонаж\n\n'+ 
            '\n'.join(map(str, CHARACTERS)) +'\n\nЧтобы получить информацию о персонаже, введите его название')
        
        if (message.chat.id in players_id):
            if(players_names[players_id.index(message.chat.id)] != message.from_user.first_name):
                players_names[players_id.index(message.chat.id)] = message.from_user.first_name

        if (message.chat.id in waiters_id):
            if(waiters_names[waiters_id.index(message.chat.id)] != message.from_user.first_name):
                waiters_names[players_id.index(message.chat.id)] = message.from_user.first_name
        
        if game_Is_Started:
          
            if len(players_id) >= 3 and (len(players_id) <= 7):
                
                if rounds_start:

                    if games_start:
                        draft_quarts()
                        games_start = False

                    draft3_7()

                    time.sleep(1)
                    
                    if len(players_id) != 7 and (len(players_id) != 3):
                        send_to_all_membs('Раунд 1 \n\nОткрытые карты: \n' + '\n'.join(map(str, OPENED_CARDS)) + '\n\n' + 'Закрытая карта: 🃏', key.keyboard7)

                    time.sleep(1)

                    send_to_all_membs('Владелец короны: ' + players_names[0] + ' 👑\n\n' + 'Очередь выбора персонажей:\n' + '\n'.join(map(str, players_names)), key.keyboard7)
                    
                    rounds_start = False

                reload_keyboard()

                char_chosen(message.text, message.chat.id)
                
                your_turn()

            elif len(players_id) == 2:
                
                if rounds_start:
                    
                    if games_start:
                        draft_quarts()
                        games_start = False

                    time.sleep(1)

                    draft2()

                    time.sleep(1)

                    send_to_all_membs('Раунд 1 \n' + 'Владелец короны: ' + players_names[0] + ' 👑\n\n', key.keyboard7)

                    rounds_start = False

                if ((('1️⃣ '+'ассасин ' + chr(0x1F977) == message.text.lower()) or
                    ('2️⃣ '+'вор ' + chr(0x1F9B9)== message.text.lower()) or
                    ('3️⃣ '+'чародей ' + chr(0x1F9D9)== message.text.lower()) or
                    ('4️⃣ '+'король ' +  chr(0x1F934) == message.text.lower()) or
                    ('5️⃣ '+'епископ '  + chr(0x1F473) == message.text.lower()) or
                    ('6️⃣ '+'купец '  + chr(0x1F935) == message.text.lower()) or
                    ('7️⃣ '+'зодчий '  + chr(0x1F477) == message.text.lower()) or
                    ('8️⃣ '+'кондотьер '  +  chr(0x1F482) == message.text.lower())) and
                    (message.chat.id == players_id[draft_index]) and
                    (message.text in ACTIVE_CHARS) and choising):

                                
                    ACTIVE_CHARS.remove(message.text)
                    ACTIVE_CHARS.sort()

                    Players[draft_index].chars.append(message.text)

                    bot.send_message(players_id[draft_index], 'Отлично!\nОдин из ваших персонажей ' + message.text, reply_markup = keyboard8)
                                        
                    reload_keyboard()

                    if len(ACTIVE_CHARS) < 6 and (len(ACTIVE_CHARS) > 1):
                        bot.send_message(players_id[draft_index], 'Выберите персонажа, которого хотите закрыть', reply_markup = keyboard8)
                        choising = False
                    elif (len(ACTIVE_CHARS) == 1):
                        ACTIVE_CHARS.clear()
                        send_to_all_membs('Выбор персонажей закончен!', key.keyboard7)
                        playing = True
                    else:
                        draft_start = True
                        draft_index = not draft_index
                            
                if ((('1️⃣ '+'ассасин ' + chr(0x1F977) == message.text.lower()) or
                    ('2️⃣ '+'вор ' + chr(0x1F9B9)== message.text.lower()) or
                    ('3️⃣ '+'чародей ' + chr(0x1F9D9)== message.text.lower()) or
                    ('4️⃣ '+'король ' +  chr(0x1F934) == message.text.lower()) or
                    ('5️⃣ '+'епископ '  + chr(0x1F473) == message.text.lower()) or
                    ('6️⃣ '+'купец '  + chr(0x1F935) == message.text.lower()) or
                    ('7️⃣ '+'зодчий '  + chr(0x1F477) == message.text.lower()) or
                    ('8️⃣ '+'кондотьер '  +  chr(0x1F482) == message.text.lower())) and
                    (message.chat.id == players_id[draft_index]) and
                    (message.text in ACTIVE_CHARS)):

                    bot.send_message(players_id[draft_index], message.text + 'не играет в этом раунде', reply_markup = key.keyboard7)
                            
                    ACTIVE_CHARS.remove(message.text)
                    ACTIVE_CHARS.sort()

                    draft_index = not draft_index 

                    reload_keyboard()

                    draft_start = True

                    choising = True
                
                reload_keyboard()

                your_turn()
            
            if playing:
                for player in Players:
                    if CHARACTERS[0] in player.chars:
                        send_to_all_membs(CHARACTERS[0] +' уже заточил свои ножи...') 

bot.polling(none_stop = True)

