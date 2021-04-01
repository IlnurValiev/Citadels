
import telebot
import random as ran
import time
import quarters as q
import keyboards as key
import requests

TG_TOKEN = '1648834181:AAHnaFSNiQSx5LEWVhKRL4N9I2t4P3q8pFw'
bot = telebot.TeleBot(TG_TOKEN)

class Player():
    def __init__(self):
        self.name = ''
        self.id = ''
        self.chars = []
        self.quarts = []
        self.b_quarts = []
        self.coins = 0
        self.score = 0
    
    def __str__(self):
        return (self.name + self.coins*'🏅' + len(self.quarts)*'🃏' + '\n' + '\n'.join(map(str, self.b_quarts))+'\n\n')

    def add_quart(self, quart):
        self.quarts.append(quart)

cur_player = Player()

thief = Player()

destr_player = Player()

grave_owner = Player()

first_builder = Player()

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

OPENED_CARDS = []

players_id = []

players_names = []

start_voters = []

Players = []

waiters_names = []

selected_chars = []

waiters_id = [] 

taken_cards = []

CLOSED_CARD = []

robbed_char = ''

destr_quart = ''

choising = True

rounds_start = True 

draft_start = True

games_start = True

moves_start = True

spec_feat = True

quart_building = True

coins_or_cards = True

start_sync = True

mes_sync = True

collect_coins = False

playing = False

swapping = False

game_Is_Started = False

quart_choising = False

enough_coins = False

char_feat = False

taking_cards = False

killing = False

stealing = False

swap_player = False

player_destr = False

quart_destr = False

have_type_q = False

lab = False

using_lab = False

smithy = False

grave = False

last_round = False

arch_builds = 3

round_index = 1

destr_cost = 1

char_index = 0

draft_index = 0

remove_keyboard = telebot.types.ReplyKeyboardRemove(True)

keyboard8 = telebot.types.ReplyKeyboardRemove(True)

keyboard9 = telebot.types.ReplyKeyboardMarkup(True)

keyboard12 = telebot.types.ReplyKeyboardMarkup(True)

def kill_steal_keyboard():
    
    global keyboard12
    global CLOSED_CARD

    keyboard12 = telebot.types.ReplyKeyboardMarkup(True)

    for i in range(CHARACTERS.index(selected_chars[char_index]) + 1, len(CHARACTERS)):
       if CHARACTERS[i] not in CLOSED_CARD and ( CHARACTERS[i] not in OPENED_CARDS):
           keyboard12.row(CHARACTERS[i])

def swap_keyboard():
    global keyboard12

    keyboard12 = telebot.types.ReplyKeyboardMarkup(True)

    if swapping:
        keyboard12.row('У игрока 👤')
        keyboard12.row('Из колоды 📤')

    if swap_player:
        for player in Players:
            if player.id != cur_player.id:
                keyboard12.row(player.name)

    keyboard12.row('Отмена')

def reload_keyboard():
    global keyboard8
    
    keyboard8 = telebot.types.ReplyKeyboardMarkup(True)

    if playing:
        keyboard8.row('Мое состояние 👤')

    keyboard8.row('Игроки 👥','Персонажи 🎭')
    
    for i in range(0, len(ACTIVE_CHARS), 2):
        if (i+1) == len(ACTIVE_CHARS):
            keyboard8.row(ACTIVE_CHARS[i])
        else:
            keyboard8.row(ACTIVE_CHARS[i], ACTIVE_CHARS[i+1])

    keyboard8.row('Выход')

def draft3_7():
    
    global ACTIVE_CHARS
    global OPENED_CARDS
    global CLOSED_CARD

    if len(players_id) != 7 and (len(players_id) != 3):
        CLOSED_CARD = []
        CLOSED_CARD.append(ran.choice(ACTIVE_CHARS))
        ACTIVE_CHARS.remove(CLOSED_CARD[0])
            
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
            if player in waiters_id:
                bot.send_message(player, message, reply_markup = key.keyboard7)
            else:
                bot.send_message(player, message, reply_markup = keyboard)

def your_turn():
    global draft_start
    global ACTIVE_CHARS
    global CLOSED_CARD

    if draft_index == 6:
        ACTIVE_CHARS += CLOSED_CARD
        ACTIVE_CHARS.sort()

    if draft_start and (draft_index < len(players_id)):
        bot.send_message(players_id[draft_index], 'Ваша очередь выбрать персонажа.\nНажмите на кнопку, чтобы это сделать.', reply_markup = keyboard8)

        for i in range(len(players_id)):
            if i != draft_index:
                bot.send_message(players_id[i], players_names[draft_index] + ' выбирает персонажа', reply_markup = key.keyboard7)

        for player in waiters_id:
            bot.send_message(player, players_names[draft_index] + ' выбирает персонажа', reply_markup = key.keyboard7)

        draft_start = False
        CLOSED_CARD = []

def draft_quarts():

    for player in Players:
        for k in range(0,4):
            _rand_quart = ran.choice(q.quarts)
            player.add_quart(_rand_quart)
            q.quarts.remove(_rand_quart)

        bot.send_message(player.id, 'Кварталы у Вас на руках:\n\n'+'\n'.join(map(str, player.quarts)))

def char_chosen(message, chat_id):
        
        message = str(message)

        global draft_start
        global draft_index
        global ACTIVE_CHARS
        global playing
        global selected_chars
        global moves_start

        if ((('1️⃣ '+'ассасин ' + chr(0x1F977) == message.lower()) or
                ('2️⃣ '+'вор ' + chr(0x1F9B9)== message.lower()) or
                ('3️⃣ '+'чародей ' + chr(0x1F9D9)== message.lower()) or
                ('4️⃣ '+'король ' +  chr(0x1F934) == message.lower()) or
                ('5️⃣ '+'епископ '  + chr(0x1F473) == message.lower()) or
                ('6️⃣ '+'купец '  + chr(0x1F935) == message.lower()) or
                ('7️⃣ '+'зодчий '  + chr(0x1F477) == message.lower()) or
                ('8️⃣ '+'кондотьер '  +  chr(0x1F482) == message.lower())) and
                (chat_id == players_id[draft_index]) and 
                (message in ACTIVE_CHARS)):

            bot.send_message(players_id[draft_index], 'Отлично!\nВ этом раунде вы ' + message, reply_markup = key.keyboard7)

            for player in Players:
                if player.id == chat_id:
                    player.chars.append(message)
            
            selected_chars.append(message)
            selected_chars.sort()
                       
            ACTIVE_CHARS.remove(message)
            ACTIVE_CHARS.sort()
                    
            draft_index = (draft_index + 1)%len(players_id)

            if len(ACTIVE_CHARS) == 1:
                send_to_all_membs("Выбор персонажей закончен")
                moves_start = True
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

def reload_play_keyboard():

    global keyboard9

    keyboard9 = telebot.types.ReplyKeyboardMarkup(True)

    keyboard9.row('Мое состояние 👤' )

    keyboard9.row('Игроки 👥', 'Персонажи 🎭')
    
    if coins_or_cards:
        keyboard9.row('Монеты 🏅🏅', 'Карты 🃏🃏')

    if quart_building and enough_coins and (arch_builds > 0) and len(cur_player.quarts):
        keyboard9.row('Построить квартал 🔨')

    if spec_feat:

        if selected_chars[char_index] == CHARACTERS[0]:
            keyboard9.row('Убить персонажа 🗡')
        
        if selected_chars[char_index] == CHARACTERS[1]:
            keyboard9.row('Обворовать персонажа 💰')

        if selected_chars[char_index] == CHARACTERS[2]:
            keyboard9.row('Обменять карты 🔃🃏')

        if selected_chars[char_index] == CHARACTERS[7]:
            keyboard9.row('Разрушить квартал 🪓')

    if collect_coins and have_type_q:
        keyboard9.row('Собрать монеты с квартолов 🏅')

    if lab and len(cur_player.quarts):
        keyboard9.row('Сбросить карту 🃏')

    if smithy:
        keyboard9.row('Получить кварталы 🃏')

    if char_feat and not grave:
        keyboard9.row('Завершить ход ❌')

    keyboard9.row('Выход')

def dest_player_key():
    global keyboard12

    keyboard12 = telebot.types.ReplyKeyboardMarkup(True)

    for player in Players:
        if CHARACTERS[4] not in player.chars and len(player.b_quarts) and (len(player.b_quarts) < 7):
            keyboard12.row(player.name)
    keyboard12.row('Отмена')

def dest_quart_key():
    global keyboard12

    keyboard12 = telebot.types.ReplyKeyboardMarkup(True)

    for quart in destr_player.b_quarts:
        if cur_player.coins >= quart.cost - destr_cost and (quart != q.fort):
            keyboard12.row(quart.name)
    keyboard12.row('Отмена')

def lab_key():
    global keyboard12

    keyboard12 = telebot.types.ReplyKeyboardMarkup(True)

    for quart in cur_player.quarts:
        keyboard12.row(quart.name)

    keyboard12.row('Отмена')

@bot.message_handler(commands=['start'])
def start(message):
    with open('main.jpg', 'rb') as ph:
        photo = ph.read()
    if message.chat.id not in players_id+waiters_id:
        bot.send_photo(message.chat.id, photo, caption = '''Добро пожаловать в "Цитадели"!

Игра о средневековых городах, благородстве и интригах.
    ''', reply_markup = key.keyboard1)
    else:
         bot.send_photo(message.chat.id, photo, caption = '''Добро пожаловать в "Цитадели"!

Игра о средневековых городах, благородстве и интригах.
    ''')

@bot.message_handler(content_types=['text'])
def send_text(message):
  global mes_sync

  while not mes_sync:
    pass
  
  mes_sync = False

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
  global keyboard8
  global waiters_names
  global playing
  global games_start
  global moves_start
  global coins_or_cards
  global char_feat
  global cur_player
  global char_index
  global taken_cards
  global taking_cards
  global keyboard10
  global quart_building
  global quart_choising
  global enough_coins
  global keyboard9
  global round_index
  global spec_feat
  global killing
  global stealing
  global robbed_char
  global thief
  global start_sync
  global keyboard12
  global selected_chars
  global swapping 
  global swap_player
  global arch_builds
  global player_destr
  global quart_destr
  global destr_player
  global collect_coins
  global have_type_q 
  global destr_cost
  global lab
  global using_lab
  global smithy
  global grave
  global grave_owner
  global destr_quart
  global first_builder
  global last_round

  if((game_Is_Started and
     (message.chat.id not in players_id+waiters_id)) or
    (not game_Is_Started )):

    if ((message.text.lower() == 'выход') and 
       (message.chat.id in players_id+waiters_id)):
        bot.send_message(message.chat.id, 'Вы вышли из игры', reply_markup = key.keyboard1)
        
        for player in Players:
            if player.id == message.chat.id:
                Players.remove(player)
        
        if message.chat.id in players_id:
            players_names.remove(players_names[players_id.index(message.chat.id)])
            players_id.remove(message.chat.id)

        if message.chat.id in waiters_id:
            waiters_names.remove(waiters_names[waiters_id.index(message.chat.id)])

        for player in players_id:
                if(len(players_id) > 1) and (player not in start_voters):
                    bot.send_message(player, message.from_user.first_name + ' вышел из игры', reply_markup = key.keyboard5)
                if len(players_id) == 1:
                    bot.send_message(player, message.from_user.first_name + ' вышел из игры', reply_markup = key.keyboard7)
                    start_voters.clear()            
                if (len(players_id) > 1) and (player in start_voters):
                    bot.send_message(player, message.from_user.first_name + ' вышел из игры', reply_markup = key.keyboard6_1)
        
        if message.chat.id in start_voters:
            start_voters.remove(message.chat.id)
    elif message.text.lower() == 'выход':
        bot.send_message(message.chat.id, 'Ok', reply_markup = key.keyboard1)

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
                for player in players_id + waiters_id:
                    if message.chat.id == player:
                        bot.send_message(message.chat.id,'Игра уже начата. Вы присоединитесь после ее окончания.')
                    else:
                        bot.send_message(player, message.from_user.first_name + ' заходит в игру, но переходит в режим ожидания и сможет присоединиться после окончания игры.')
            else:   
                players_id.append(message.chat.id)
                players_names.append(message.from_user.first_name) 
                player = Player()
                player.id = message.chat.id
                player.name = message.from_user.first_name
                player.coins = 2
                Players.append(player)       
            
                if(len(players_id) > 1):
                    bot.send_message(message.chat.id, 'Вы в игре!\n'+
                'Могут участвовать от 2 до 7 человек. Чтобы начать, введите "старт".'+
                ' Как только проголосуют все, игра начнется. \n'+
                'Список игроков: ' + ', '.join(map(str, players_names)), 
                reply_markup = key.keyboard5)
                else: 
                    bot.send_message(message.chat.id, 'Вы в игре!\n'+
                'Могут участвовать от 2 до 7 человек. Чтобы начать, введите "старт".'+
                ' Как только проголосуют все, игра начнется. \n'+
                'Список игроков: ' + ', '.join(map(str, players_names)), 
                reply_markup = key.keyboard7)
                
            for player in (players_id + waiters_id):
                if player != message.chat.id:
                    if message.chat.id in waiters_id:
                        bot.send_message(player, message.from_user.first_name + ' присоединяется к игре')
                    else:
                        if player not in start_voters:
                            bot.send_message(player, message.from_user.first_name + ' присоединяется к игре', reply_markup = key.keyboard5)
                        else:
                            bot.send_message(player, message.from_user.first_name + ' присоединяется к игре')
   
    if((message.text.lower() == 'старт' or (message.text.lower() == 'старт 🙋‍♂️')) and (message.chat.id in players_id) and
      (message.chat.id not in start_voters)):

        if(len(players_id) == 1):
          bot.send_message(message.chat.id, 'Недостаточно игроков для начала игры.')        
        
        else:


                start_voters.append(message.chat.id)    
                
                for player in players_id:
                    if(message.chat.id != player):
                        bot.send_message(player, message.from_user.first_name +
                    ' голосует за начало игры.\n\n' +
                    'Всего голосов: ' +
                    str(len(start_voters))+'/'+str(len(players_id)))
                    else:
                        bot.send_message(player, 'Вы проголосовали. Чтобы отменить свой голос, введите "отмена".\n\n' +
                    'Всего голосов: ' +
                    str(len(start_voters))+'/'+str(len(players_id)),
                    reply_markup = key.keyboard6_1)

    elif((message.text.lower() == 'старт' or
         (message.text.lower() == 'старт 🙋‍♂️')) and
         (message.chat.id in players_id)):
        bot.send_message(message.chat.id,'Вы уже проголосовали. Для отмены голоса введите "отмена"')

    if len(start_voters) == len(players_id) and (len(players_id) > 1) and not game_Is_Started:
        game_Is_Started = True
        start_voters.clear()
        send_to_all_membs('Проголосовали все!\nИгра началась!',key.keyboard7)

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
        bot.send_message(message.chat.id, 'Вы можете скачать правила в формате pdf, посмотреть видео, а также открыть список персонажей или кварталов.\nОсобенности и отличия от настольной версии:\n— игроки выбирают персонажей в порядке входа в игру, т. е. первый вошедший получает корону, и тд в порядке присоединения в игру.\n— если у вас не хватает монет на постройку ни одного из кварталов или карт на руке нет, то кнопки постройки кварталов не будет. Аналогично для свойств особых кварталов, позволяющих обменивать монеты на кварталы и наоборот.\n — квартал призраков(в конце игры считается кварталом любого типа на выбор) работает несколько иначе: если в конце вам не будет хватать только одного типа кварталов, то квартал призраков засчитывается за недостающий тип.',
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
        '\n'.join(map(str, CHARACTERS)))

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
        try:
            if(players_names[players_id.index(message.chat.id)] != message.from_user.first_name):
                players_names[players_id.index(message.chat.id)] = message.from_user.first_name
        except IndexError:
            pass

  if game_Is_Started and (message.chat.id in players_id+waiters_id):

        if ((message.text.lower() == 'выход') and 
            (message.chat.id in players_id+waiters_id)):
            
            bot.send_message(message.chat.id, 'Вы вышли из игры', reply_markup = key.keyboard1)

            for player in Players:
                if player.id == message.chat.id:
                    Players.remove(player)
                    q.quarts += player.quarts + player.b_quarts 
                    
            if message.chat.id == cur_player.id and not grave:
                char_feat = False

            if message.chat.id == grave_owner.id and grave:
                    char_feat = False
            if len(selected_chars):
                if selected_chars[char_index] == CHARACTERS[7] and grave:
                    coins_or_cards = False
                    quart_building = False
                    spec_feat =  False 
                    collect_coins = False 
                    lab = False 
                    smithy = False
            
            if (message.chat.id == players_id[draft_index]) and not playing:
                draft_start = True

            reload_keyboard()

            if message.chat.id in players_id:        
                players_names.remove(players_names[players_id.index(message.chat.id)])
                players_id.remove(message.chat.id)              
            else:
                waiters_id.remove(message.chat.id)

            for player in players_id+waiters_id:
                bot.send_message(player, message.from_user.first_name + ' вышел из игры')             
                                
            if(len(players_id) == 1):
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
                CLOSED_CARD = []
                OPENED_CARDS.clear()
                draft_index = 0
                rounds_start = True 
                draft_start = True
                playing = False
                games_start = True
                selected_chars = []
                moves_start = True
                char_feat = False
                taken_cards.clear()
                taking_cards = False
                cur_player = Player()
                char_index = 0
                coins_or_cards = True
                taken_cards = []
                games_start = True
                quart_building = True
                round_index = 1
                quart_choising = False
                enough_coins = False 
                start_voters.clear()
                arch_builds = 3
                last_round = False

                Players[0].coins = 2
                Players[0].chars = []
                Players[0].quarts = []
                Players[0].b_quarts = []

                q.quarts = []
                for quart in q.QUARTS:
                    q.quarts.append(quart)

                players_id += waiters_id
                players_names = players_names + waiters_names
                waiters_id.clear()
                waiters_names.clear()
               
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
                (message.text not in CHARACTERS) and
                (message.text not in q.quarts_names) and
                (message.text != 'Карты 🃏🃏') and
                (message.text != 'Завершить ход ❌') and
                (message.text != 'Построить квартал 🔨') and
                (message.text != 'Монеты 🏅🏅' ) and
                (message.text != 'Отмена') and
                (message.text != 'Мое состояние 👤') and 
                (message.text != 'Убить персонажа 🗡') and
                (message.text != 'Обворовать персонажа 💰') and
                (message.text != 'Разрушить квартал 🪓') and
                (message.text != 'Собрать монеты с квартолов 🏅') and
                (message.text != 'У игрока 👤') and 
                (message.text != 'Из колоды 📤') and
                (message.text != 'Сбросить карту 🃏') and
                (message.text != 'Взять 🃏') and
                (message.text != 'Обменять карты 🔃🃏') and
                (message.text != 'Играть 🎮') and
                (message.text not in players_names)):
                bot.send_message(player, message.from_user.first_name + ': ' + message.text)

        if message.text == 'Мое состояние 👤':
            for player in Players:
                if player.id == message.chat.id:
                    bot.send_message(player.id, 'Кварталы в руке:\n\n'+'\n'.join(map(str, player.quarts)) + '\n\nПостроенные кварталы:\n\n' + '\n'.join(map(str, player.b_quarts)) + '\n\nМонеты: ' + player.coins*'🏅')
                    break
       
        if ('игроки' == message.text.lower() or 
            'игроки 👥' == message.text.lower()):
            if len(waiters_id):
                bot.send_message(message.chat.id, 'Список игроков в порядке выбора персонажей:\n' 'имя | монеты | кварталы в руке\nпостроенные кварталы\n\n'+'\n'.join(map(str, Players)) + '\nОжидающие игроки:\n'+'\n'.join(map(str, waiters_names)))
            else:
                bot.send_message(message.chat.id, 'Список игроков в порядке выбора персонажей:\n' 'имя | монеты | кварталы в руке\nпостроенные кварталы\n\n'+'\n'.join(map(str, Players)))

        if ("персонажи 🎭" == message.text.lower()):
            bot.send_message(message.chat.id,'Очередь хода | персонаж\n\n'+ 
            '\n'.join(map(str, CHARACTERS)))
        
        if (message.chat.id in players_id):
            if(players_names[players_id.index(message.chat.id)] != message.from_user.first_name):
                players_names[players_id.index(message.chat.id)] = message.from_user.first_name
                for player in Players:
                    if message.chat.id == player.id:
                        player.name = message.from_user.first_name

        if (message.chat.id in waiters_id):
            if(waiters_names[waiters_id.index(message.chat.id)] != message.from_user.first_name):
                waiters_names[waiters_id.index(message.chat.id)] = message.from_user.first_name
        
        if game_Is_Started:
          
            if (len(players_id) >= 3 and (len(players_id) <= 7)):
                
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

                if ((message.text in ACTIVE_CHARS) and
                    (message.chat.id == players_id[draft_index]) and choising):
                         
                    ACTIVE_CHARS.remove(message.text)
                    ACTIVE_CHARS.sort()

                    for player in Players:
                        if player.id == message.chat.id:
                            player.chars.append(message.text)

                    selected_chars.append(message.text)
                    selected_chars.sort()

                    bot.send_message(players_id[draft_index], 'Отлично!\nОдин из ваших персонажей ' + message.text, reply_markup = keyboard8)
                                        
                    reload_keyboard()

                    if len(ACTIVE_CHARS) < 6 and (len(ACTIVE_CHARS) > 1):
                        bot.send_message(players_id[draft_index], 'Выберите персонажа, которого хотите закрыть', reply_markup = keyboard8)
                        choising = False
                    elif (len(ACTIVE_CHARS) == 1):
                        send_to_all_membs('Выбор персонажей закончен!', key.keyboard7)
                        playing = True
                        moves_start = True
                        ACTIVE_CHARS.clear()
                    else:
                        draft_start = True
                        draft_index = (draft_index + 1)%2
                            
                if ((message.chat.id == players_id[draft_index]) and
                    (message.text in ACTIVE_CHARS)):

                    bot.send_message(players_id[draft_index], message.text + ' не играет в этом раунде', reply_markup = key.keyboard7)
                            
                    ACTIVE_CHARS.remove(message.text)
                    ACTIVE_CHARS.sort()

                    draft_index = (draft_index+1)%2

                    reload_keyboard()

                    draft_start = True

                    choising = True
                
                reload_keyboard()

                your_turn()
            
            if playing:
                    if char_feat:
                        if message.chat.id == cur_player.id: 

                            if coins_or_cards:

                                if message.text == 'Монеты 🏅🏅':                           
                                    cur_player.coins = cur_player.coins + 2
                                    coins_or_cards = False
                                    
                                    enough_coins = False
                                    for quart in cur_player.quarts:
                                        if cur_player.coins >= quart.cost and (quart not in cur_player.b_quarts):
                                            enough_coins = True
                                            break
                                    
                                    if q.smithy in cur_player.b_quarts:
                                        smithy = True
                                        
                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy
                                    
                                    reload_play_keyboard()
                                    
                                    for player in players_id+waiters_id:
                                        if message.chat.id == player:
                                            bot.send_message(player, 'Вы взяли две монеты', reply_markup = keyboard9)
                                        else:
                                            bot.send_message(player, message.from_user.first_name + ' решает взять монеты.')                                    

                                if message.text == 'Карты 🃏🃏':
                                    
                                    keyboard10 = telebot.types.ReplyKeyboardMarkup(True)

                                    taken_cards = []

                                    if q.observ in cur_player.b_quarts:
                                        cards_quant = 3
                                    else:
                                        cards_quant = 2
                                                                            
                                    for i in range(0,cards_quant):             

                                        rand_quart = ran.choice(q.quarts)

                                        error = True
                                        
                                        while error:
                                            try:
                                                quart_name = rand_quart.name                    
                                            except AttributeError:
                                                rand_quart = ran.choice(q.quarts)
                                            else:
                                                error = False

                                        coins_or_cards = False
                                    
                                        reload_play_keyboard()

                                        taken_cards.append(rand_quart)

                                        q.quarts.remove(rand_quart)

                                        keyboard10.row(quart_name)

                                    if q.lib in cur_player.b_quarts:
                                        cur_player.quarts += taken_cards
                                        
                                        char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (have_type_q and collect_coins) or lab or smithy

                                        reload_play_keyboard()

                                        for player in players_id+waiters_id:
                                            if message.chat.id == player:
                                                bot.send_message(cur_player.id, 'Вы берете на руку:\n\n'+
                                    '\n'.join(map(str, taken_cards)), reply_markup = keyboard9)
                                            else:
                                                bot.send_message(player, message.from_user.first_name+' решает взять карты')
                                    else:
                                        taking_cards = True
                                        for player in players_id+waiters_id:
                                            if message.chat.id == player:
                                                bot.send_message(cur_player.id, 'Взятые кварталы:\n'+
                                        '\n'.join(map(str, taken_cards))+ '\nВыберите один из них', reply_markup = keyboard10)
                                            else:
                                                reload_play_keyboard()
                                                bot.send_message(player, message.from_user.first_name+' решает взять карты')
 
                            if taking_cards:
                                for card in taken_cards:                                   
                                    if message.text == card.name:
                                        
                                        cur_player.quarts.append(card)

                                        for quart in cur_player.quarts:
                                            if cur_player.coins >= quart.cost:
                                                enough_coins = True
                                                break
                                                
                                        char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (have_type_q and collect_coins) or lab or smithy
                                        
                                        reload_play_keyboard()
                                        
                                        taken_cards.remove(card)
                                                                               
                                        q.quarts.append(taken_cards)
                                        
                                        taking_cards = False
 
                                        bot.send_message(cur_player.id, card.name + ' теперь у Вас на руках.', reply_markup = keyboard9)
                                        
                            if quart_building:
                                    if message.text == 'Построить квартал 🔨':
                                        keyboard11 = telebot.types.ReplyKeyboardMarkup(True)
                                        
                                        for quart in cur_player.quarts:
                                            while True:
                                                try:
                                                    if cur_player.coins >= quart.cost and (quart not in cur_player.b_quarts):
                                                        keyboard11.row(quart.name)
                                                    break
                                                except AttributeError:
                                                    pass

                                        keyboard11.row('Отмена')

                                        bot.send_message(cur_player.id, 'Выберите квартал, который хотите построить\n'+'\nВаши кварталы:\n'+'\n'.join(map(str, cur_player.quarts)) + '\n\nМонеты:' +cur_player.coins*'🏅', reply_markup = keyboard11)
                                    
                                        quart_choising = True
                            
                            if quart_choising:
                                for quart in cur_player.quarts:
                                    if message.text == quart.name:
                                            if quart not in cur_player.b_quarts:
                                                if(cur_player.coins >= quart.cost):


                                                    cur_player.b_quarts.append(quart)
                                                    cur_player.quarts.remove(quart)
                                                    cur_player.coins -= quart.cost

                                                    enough_coins = False
                                                    for _quart in cur_player.quarts:
                                                        if cur_player.coins >= _quart.cost and (_quart not in cur_player.b_quarts):
                                                            enough_coins = True
                                                            break
                                                  
                                                    if q.lab in cur_player.b_quarts:
                                                        lab = True

                                                    smithy = False
                                                    if q.smithy in cur_player.b_quarts and (cur_player.coins >= 2):
                                                        smithy = True

                                                    if q.grave in cur_player.b_quarts:
                                                        grave_owner = cur_player

                                                    quart_choising = False

                                                    if selected_chars[char_index] == CHARACTERS[6]:
                                                        arch_builds -= 1
                                                    
                                                    if selected_chars[char_index] != CHARACTERS[6] or not arch_builds:

                                                        quart_building = False

                                                        if selected_chars[char_index] == CHARACTERS[3]:
                                                            if quart.type == '🟡':
                                                                have_type_q = True
        
                                                        if selected_chars[char_index] == CHARACTERS[4]:
                                                            if quart.type == '🔵':
                                                                have_type_q = True
                                                        if selected_chars[char_index] == CHARACTERS[5]:
                                                            if quart.type == '🟢':
                                                                have_type_q = True
                                                        if selected_chars[char_index] == CHARACTERS[7]:
                                                            if quart.type == '🔴':
                                                                have_type_q = True
                                                            
                                                        if quart == q.hogwarts:
                                                            have_type_q = True                                            
                                                    
                                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy

                                                    reload_play_keyboard()

                                                    for player in players_id+waiters_id:
                                                        if player == message.chat.id:
                                                            bot.send_message(player, 'Отлично! Вы построили:\n' + str(quart), reply_markup = keyboard9)
                                                        else:
                                                            bot.send_message(player, message.from_user.first_name + ' строит себе:\n' + str(quart))

                                                    if len(cur_player.b_quarts) == 7 and (first_builder.name == ''):
                                                        last_round = True
                                                        first_builder = cur_player
                                                        send_to_all_membs(cur_player.name + ' строит седьмой квартал и достраивает город, поэтому этот раунд будет последним в игре. Кондотьер не может разрушать здания в достроенном городе')

                                                else:
                                                    bot.send_message(cur_player.id, 'У вас недостаточно монет для постройки. Выберите другой квартал или накопите больше монет.')

                                if message.text == 'Отмена':
                                    quart_choising = False
                                    bot.send_message(cur_player.id, 'Ваш ход. Нажмите на кнопку, чтобы выполнить действие', reply_markup = keyboard9)

                            if spec_feat:
                                if selected_chars[char_index] == CHARACTERS[0]:
                                    if message.text == 'Убить персонажа 🗡':
                                        
                                        kill_steal_keyboard()
                                        
                                        bot.send_message(cur_player.id, 'Выберите персонажа, которого хотите убить', reply_markup = keyboard12)

                                        killing = True
                                        spec_feat = False
                                
                                if selected_chars[char_index] == CHARACTERS[1]:
                                    if message.text == 'Обворовать персонажа 💰':

                                        kill_steal_keyboard()

                                        bot.send_message(cur_player.id, 'Выберите персонажа, которого хотите обворовать', reply_markup = keyboard12)

                                        stealing = True
                                        spec_feat = False

                                if selected_chars[char_index] == CHARACTERS[2]:
                                    if message.text == 'Обменять карты 🔃🃏':
                                        swapping = True

                                        swap_keyboard()

                                        bot.send_message(cur_player.id, 'Выберите, обменять на краты из колоды или с руки другого игрока', reply_markup = keyboard12)
                                        
                                        spec_feat = False
                                
                                if selected_chars[char_index] == CHARACTERS[7]:
                                    if message.text == 'Разрушить квартал 🪓':
                                        
                                        dest_player_key()
                                        
                                        bot.send_message(cur_player.id, 'Выберие игрока, у когорого хотите разрушить квартал. Вы не можете разрушить кварталы епископа.',reply_markup = keyboard12)

                                        player_destr = True

                                        spec_feat = False

                            if killing:
                                if message.text in CHARACTERS and (message.text not in OPENED_CARDS):
                                    
                                    if message.text in selected_chars:
                                        selected_chars.remove(message.text)
                                        CLOSED_CARD.append(message.text)    

                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy

                                    reload_play_keyboard()

                                    for player in players_id+waiters_id:
                                        if player == message.chat.id:
                                            bot.send_message(player, message.text + ' убит ассасином и не играет в этом раунде', reply_markup = keyboard9)
                                        else:
                                            bot.send_message(player, message.text + ' убит ассасином и не играет в этом раунде')

                                    killing = False
                                  
                            if stealing:
                                if message.text in CHARACTERS and (message.text not in OPENED_CARDS) and (message.text not in CLOSED_CARD):

                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy

                                    reload_play_keyboard()

                                    for player in players_id+waiters_id:
                                        if player == message.chat.id:
                                            bot.send_message(player, message.text + ' обворован и в свой ход он передаст вору все свои монеты', reply_markup = keyboard9)
                                        else:
                                            bot.send_message(player, message.text + ' обворован и в свой ход он передаст вору все свои монеты')

                                    robbed_char = message.text

                                    thief = cur_player
                                    
                                    stealing = False

                            if swapping:
                                if message.text == 'У игрока 👤':
                                    swap_player = True
                                    swapping = False
                                    
                                    
                                    swap_keyboard()

                                    bot.send_message(cur_player.id, 'Выберите, с руки какого игрока хотите обменять карты', reply_markup = keyboard12)

                                if message.text == 'Из колоды 📤':
                                    taken_cards = []
                                    
                                    for i in range(0,len(cur_player.quarts)):
                                        rand__quart = ran.choice(q.quarts)
                                        taken_cards.append(rand__quart)
                                        q.quarts.remove(rand__quart)
                                    
                                    q.quarts += cur_player.quarts
                                    cur_player.quarts = taken_cards
                                    
                                    enough_coins = False

                                    spec_feat = False

                                    for quart in cur_player.quarts:
                                        if cur_player.coins >= quart.cost:
                                            enough_coins = True
                                            break

                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy

                                    reload_play_keyboard() 

                                    for player in players_id+waiters_id:
                                        if player != cur_player.id:
                                            bot.send_message(player, cur_player.name + ' меняет свои кварталы на карты из колоды')
                                        else:
                                            bot.send_message(cur_player.id, 'Вы взяли из колоды:\n' + '\n'.join(map(str, taken_cards)), reply_markup = keyboard9)
                                
                                if message.text == 'Отмена':
                                    swapping = False
                                    spec_feat = True
                                    reload_play_keyboard()

                                    bot.send_message(cur_player.id, 'Ваш ход. Нажмите на кнопку, чтобы выполнить действие', reply_markup = keyboard9)

                            if swap_player:
                                for player in Players:
                                    if player.id != message.chat.id:
                                        if player.name == message.text:                                                                           
                                            reload_play_keyboard()

                                            player.quarts, cur_player.quarts = cur_player.quarts, player.quarts
                                            
                                            bot.send_message(cur_player.id, 'Вы обмениваетесь картами с игроком ' + player.name + ' и получаете:\n\n'+'\n'.join(map(str, cur_player.quarts)), reply_markup = keyboard9)

                                            bot.send_message(player.id, cur_player.name + ' обменивается с Вами картами, и вы получаете:\n\n'+'\n'.join(map(str, player.quarts)))
                                            
                                            for player_Id in players_id+waiters_id:
                                                if player_Id != message.chat.id and (player_Id != player.id):
                                                    bot.send_message(player_Id, cur_player.name + ' обменивается картами с ' + player.name)
                                            
                                            swap_player = False

                                            spec_feat = False

                                            enough_coins = False

                                            for quart in cur_player.quarts:
                                                if cur_player.coins >= quart.cost:
                                                    enough_coins = True
                                                    break
                                        
                                            break
                                
                                if message.text == 'Отмена':
                                    swapping = True

                                    swap_player = False

                                    swap_keyboard()

                                    bot.send_message(cur_player.id, 'Выберите, обменять на краты из колоды или с руки другого игрока', reply_markup = keyboard12)

                            if player_destr:
                                for player in Players:
                                    if CHARACTERS[4] not in player.chars:
                                        if message.text == player.name and len(player.b_quarts) and (len(player.b_quarts) < 7):
                                            
                                            quart_destr = True

                                            player_destr = False

                                            destr_player = player

                                            if q.great_wall in player.b_quarts:
                                                destr_cost = 0
                                            else:
                                                destr_cost = 1

                                            dest_quart_key()

                                            bot.send_message(cur_player.id, 'Построенные кварталы игрока:\n\n' + '\n'.join(map(str, player.b_quarts)) + '\n\nВаши монеты: ' + cur_player.coins*'🏅'+'\n\n Выберите квартал из доступных, который хотите разрушить. Стоимость разушения на одну монету меньше стоимости квартала.', reply_markup = keyboard12)

                                if message.text =='Отмена':
                                    player_destr = False
                                    spec_feat = True
                                    quart_destr = False

                                    reload_play_keyboard()

                                    bot.send_message(message.chat.id,'Ваш ход. Нажмите на кнопку, чтобы выполнить действие', reply_markup = keyboard9)

                            if quart_destr:
                                for quart in destr_player.b_quarts:
                                    if quart.name == message.text and (quart != q.fort):
                                       
                                        if cur_player.coins >= quart.cost - destr_cost:
                                            
                                            cur_player.coins -= quart.cost - destr_cost
                                            
                                            destr_player.b_quarts.remove(quart)

                                            enough_coins = False
                                            for _quart in cur_player.quarts:
                                                if cur_player.coins >= _quart.cost:
                                                    enough_coins = True
                                                    break

                                            reload_play_keyboard()
                                            
                                            for player in players_id+waiters_id:
                                                if message.chat.id != player:
                                                    bot.send_message(player, 'Кондотьер разрушает:\n' + str(quart) + '\nу игрока ' + destr_player.name)
                                                else:
                                                    bot.send_message(player, 'Вы разрушили'  + ' у игрока ' + destr_player.name +'\n'+ str(quart), reply_markup = keyboard9)
                                            
                                            if q.grave in grave_owner.b_quarts:
                                                if grave_owner.coins >= 1:
                                                    grave = True

                                                    destr_quart = quart

                                                    grave_keyboard = telebot.types.ReplyKeyboardMarkup(True)

                                                    grave_keyboard.row('Взять')
                                                    grave_keyboard.row('Отмена')

                                                    bot.send_message(grave_owner.id, "Вы можете взять на руку разрушенный квартал за одну монету",reply_markup = grave_keyboard)

                                                    send_to_all_membs("Ход может завершиться только после того, как владелец кладбища решит, брать ли разрушенный квартал.")
                                            
                                            quart_destr = False
                                            player_destr = False
                                            
                                            char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy
                                
                                if message.text == 'Отмена':
                                    player_destr = True
                                    quart_destr = False

                                    dest_player_key()

                                    bot.send_message(cur_player.id, 'Выберие игрока, у когорого хотите разрушить квартал. Вы не можете разрушить кварталы епископа.',reply_markup = keyboard12)

                            if collect_coins:
                                if message.text == 'Собрать монеты с квартолов 🏅':
                                    
                                    if q.hogwarts in cur_player.b_quarts:
                                        collected_coins = 1
                                    else:
                                        collected_coins = 0

                                    collect_coins = False
                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy

                                    reload_play_keyboard()

                                    for quart in cur_player.b_quarts:                                        
                                        if selected_chars[char_index] == CHARACTERS[3]:
                                            if quart.type == '🟡':
                                                
                                                collected_coins += 1
                                        
                                        if selected_chars[char_index] == CHARACTERS[4]:
                                            if quart.type == '🔵':
                                                
                                                collected_coins += 1

                                        if selected_chars[char_index] == CHARACTERS[5]:
                                            if quart.type == '🟢':
                                                collected_coins += 1

                                        if selected_chars[char_index] == CHARACTERS[7]:
                                            if quart.type == '🔴':
                                                
                                                collected_coins += 1
                                        
                                    cur_player.coins += collected_coins

                                    for player in players_id+waiters_id:
                                        if player == message.chat.id:
                                            bot.send_message(player, 'Вы собрали монеты с кварталов своего типа: ' + collected_coins*'🏅', reply_markup = keyboard9)
                                        else:
                                            bot.send_message(player, cur_player.name + ' собирает монеты с кварталов своего типа: ' + collected_coins*'🏅')

                            if message.text == 'Завершить ход ❌' and not grave:
                                char_feat = False
                            
                            if lab:
                                if message.text == 'Сбросить карту 🃏':
                                    using_lab = True

                                    lab_key()

                                    bot.send_message(message.chat.id, 'Выберите квартал, который хотите обменять на 2 монеты', reply_markup = keyboard12)
                            
                            if using_lab:
                                for quart in cur_player.quarts:
                                    if message.text == quart.name:
                                        cur_player.quarts.remove(quart)
                                        q.quarts.append(quart)
                                        cur_player.coins += 2
                                        
                                        lab = False
                                        using_lab = False

                                        reload_play_keyboard()

                                        for player in players_id+waiters_id:
                                            if player == message.chat.id:
                                                bot.send_message(player, 'Вы сбросили карту и получили 2 монеты 🏅🏅', reply_markup = keyboard9)
                                            else:
                                                bot.send_message(player, cur_player.name + ' сбрасывает карту и получает 2 монеты благодаря лаборатории')

                                if message.text == 'Отмена':
                                    lab = True
                                    using_lab = False

                                    reload_play_keyboard()

                                    bot.send_message(cur_player.id, 'Вы отменили сброс карт', reply_markup = keyboard9)

                            if smithy:
                                if message.text == 'Получить кварталы 🃏':
                                    cur_player.coins -= 2
                                    
                                    rand_quarts = []

                                    for i in range(3):
                                        __rand_quart = ran.choice(q.quarts)
                                        cur_player.quarts.append(__rand_quart)
                                        q.quarts.remove(__rand_quart)
                                        rand_quarts.append(__rand_quart)

                                    smithy = False

                                    char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy

                                    reload_play_keyboard()

                                    for player in players_id+waiters_id:
                                        if player == message.chat.id:
                                            bot.send_message(player, 'Вы заплатили 🏅🏅 и получили:\n\n'+'\n'.join(map(str, rand_quarts)), reply_markup = keyboard9)
                                        else:
                                            bot.send_message(player, cur_player.name + ' благодаря кузне платит 🏅🏅 и получает 3 карты кварталов в руку')
                           
                        if message.chat.id == grave_owner.id and grave:
                            if message.text == 'Взять':
                                grave_owner.coins -= 1
                                grave_owner.quarts.append(destr_quart)
                                
                                grave_keyboard = telebot.types.ReplyKeyboardMarkup(True)
                                grave_keyboard.row('Мое состояние 👤' )
                                grave_keyboard.row('Игроки 👥', 'Персонажи 🎭')
                                grave_keyboard.row('Выход')

                                for player in players_id+waiters_id:
                                    if player == grave_owner.id:
                                        bot.send_message(player,'Вы забрали себе разрушенный квартал', reply_markup = grave_keyboard)
                                    else:
                                        bot.send_message(player, grave_owner.name + ' забирает себе в руку разрушенный квартал')

                                grave = False
                                char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy
                            if message.text == 'Отмена':
                                grave = False
                                char_feat = coins_or_cards or grave or (quart_building and enough_coins) or spec_feat or (collect_coins and have_type_q) or lab or smithy
                                send_to_all_membs(grave_owner.name+' отказывается брать разрушенный квартал')

                    if not char_feat and not moves_start:
                            if char_index == (len(selected_chars) - 1):
                                if last_round:

                                    playing = False

                                    game_Is_Started = False

                                    winners = []

                                    stats = []

                                    first_builder.score += 4
   
                                    for player in Players:
                                        types = []

                                        for quart in player.b_quarts:
                                            
                                            player.score += quart.cost
                                            
                                            if quart == q.univer:
                                                player.score += 2

                                            if quart == q.dragon_gates:
                                                player.score += 2
                                            
                                            if quart == q.coffers:
                                                player.score += player.coins
                                            
                                            if quart == q.assem:
                                                player.score += len(player.quarts)
                                            
                                            if quart.type not in types and (quart != q.ghost):
                                                types.append(quart.type)
                                        
                                        if q.ghost in player.b_quarts:
                                            if len(types) == 4:
                                                types.append('🟣')

                                        if len(player.b_quarts) == 7 and (player.id != first_builder.id):
                                            player.score += 2
                                       
                                        if len(types) == 5:
                                            player.score += 3
                                        
                                        for j in range(len(Players)-1):
                                            if Players[j].score < Players[j+1].score:
                                                Players[j], Players[j+1] = Players[j+1], Players[j]

                                    send_to_all_membs('Все персонажи выполнили свои действия.\n\nИгра окончена.\n\nПодсчет очков происходит по следующей схеме: \n• каждому игроку начисляется столько очков, какова суммарная стоимость всех кварталов его города;\n• если у игрока в городе есть кварталы всех пяти видов, он получает 3 бонусных очка; \n• если игрок первым достроил город, он получает 4 бонусных очка;\n• если игрок успел достроить город (но не первым), он получает 2 бонусных очка;\n• карты бонусных кварталов приносят игрокам очки согласно тексту на них.', key.keyboard5)
                                    
                                    send_to_all_membs('Итоги игры:\n\n'+'\n'.join(map(str, Players)))
                                    
                                    max_score = Players[0].score

                                    for player in Players:
                                        if player.score == max_score:
                                            winners.append(player.name)

                                        stats.append(player.name + '  ' + str(player.score))
                                        player.coins = 2
                                        player.chars.clear()
                                        player.quarts.clear()
                                        player.b_quarts.clear()
                                        player.score = 0

                                    send_to_all_membs('Имя | очки:\n\n'+'\n'.join(map(str, stats)))

                                    if len(winners) > 1:
                                        send_to_all_membs('Поздравляем победителей: '+', '.join(map(str, winners))+' 🥳')
                                    elif len(winners) == 1:
                                         send_to_all_membs('Поздравляем победителя: '+ winners[0]+' 🥳')

                                    send_to_all_membs('Чтобы начать новую игру, введите "старт". Как только проголосуют все, игра начнется')
                                   
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
                                    CLOSED_CARD = []
                                    OPENED_CARDS.clear()
                                    draft_index = 0
                                    rounds_start = True 
                                    draft_start = True   
                                    games_start = True
                                    selected_chars = []
                                    moves_start = False
                                    char_feat = False
                                    taken_cards.clear()
                                    taking_cards = False
                                    cur_player = Player()
                                    char_index = 0
                                    coins_or_cards = True
                                    taken_cards = []
                                    games_start = True
                                    quart_building = True
                                    round_index = 1
                                    quart_choising = False
                                    enough_coins = False 
                                    start_voters.clear()
                                    arch_builds = 3
                                    last_round = False
                                    first_builder = Player()

                                    players_id += waiters_id
                                    players_names += waiters_names

                                    for waiter in waiters_id:
                                        bot.send_message(waiter,'Вы присоединяетесь к игре.', reply_markup = key.keyboard5)
                                        player = Player()
                                        player.id = waiter
                                        player.name = waiters_names[waiters_id.index(waiter)]
                                        Players.append(player)

                                    waiters_id.clear()
                                    waiters_names.clear()

                                    q.quarts = []
                                    for quart in q.QUARTS:
                                        q.quarts.append(quart)

                                else:
                                    for player in Players:
                                        player.chars.clear() 

                                    char_index = 0

                                    round_index += 1

                                    selected_chars.clear()

                                    send_to_all_membs('Все персонажи выполнили свои действия.\n\nНачинается следующий раунд')                                    
                                    
                                    draft_start = True
                                    
                                    choising = True

                                    robbed_char = Player()

                                    arch_builds = 3
                                    
                                    ACTIVE_CHARS = [
                                        '1️⃣ '+'Ассасин ' + chr(0x1F977),
                                        '2️⃣ '+'Вор ' + chr(0x1F9B9),
                                        '3️⃣ '+'Чародей ' + chr(0x1F9D9),
                                        '4️⃣ '+'Король ' +  chr(0x1F934) ,
                                        '5️⃣ '+'Епископ '  + chr(0x1F473),
                                        '6️⃣ '+'Купец '  + chr(0x1F935),
                                        '7️⃣ '+'Зодчий '  + chr(0x1F477),
                                        '8️⃣ '+'Кондотьер '  +  chr(0x1F482)
                                        ]
                                    
                                    draft_index = 0
                                    
                                    OPENED_CARDS.clear()
                                    
                                    playing = False
                                
                                    if len(players_id) >= 3 and (len(players_id) <= 7):

                                            draft3_7()

                                            time.sleep(1)
                                            
                                            if len(players_id) != 7 and (len(players_id) != 3):
                                                send_to_all_membs('Раунд '+ str(round_index) + '\n\nОткрытые карты: \n' + '\n'.join(map(str, OPENED_CARDS)) + '\n\n' + 'Закрытая карта: 🃏', key.keyboard7)

                                            time.sleep(1)

                                            send_to_all_membs('Владелец короны: ' + players_names[0] + ' 👑\n\n' + 'Очередь выбора персонажей:\n' + '\n'.join(map(str, players_names)), key.keyboard7)
                                    
                                    elif len(players_id) == 2:
                                    
                                            draft2()

                                            time.sleep(1)

                                            send_to_all_membs('Раунд ' + str(round_index)+'\n' + 'Владелец короны: ' + players_names[0] + ' 👑\n\n', key.keyboard7)
                                    
                                    reload_keyboard()

                                    your_turn()                                                                              
                            else:   
                                    moves_start = True                           
                                    char_index = char_index + 1
                    
                    if moves_start:
                        for player in Players:
                            if selected_chars[char_index] in player.chars:


                                coins_or_cards = True
                                quart_building = True
                                enough_coins = False
                                have_type_q = False

                                char_feat = True
                                
                                spec_feat = True
                            
                                cur_player = player
                                
                                for quart in cur_player.b_quarts:
                                    if selected_chars[char_index] == CHARACTERS[3]:
                                        if quart.type == '🟡':
                                            have_type_q = True
                                            break
                                    if selected_chars[char_index] == CHARACTERS[4]:
                                        if quart.type == '🔵':
                                            have_type_q = True
                                            break
                                    if selected_chars[char_index] == CHARACTERS[5]:
                                        if quart.type == '🟢':
                                            have_type_q = True
                                            break
                                    if selected_chars[char_index] == CHARACTERS[7]:
                                        if quart.type == '🔴':
                                            have_type_q = True
                                            break
                                    if quart == q.hogwarts:
                                        have_type_q = True
                                        break
                                        
                                send_to_all_membs('Ходит: ' + selected_chars[char_index] + '\nИгрок: ' + players_names[players_id.index(player.id)], keyboard8)

                                if robbed_char == selected_chars[char_index]:
                                    send_to_all_membs('Он был обворован, поэтому передает все свои монеты вору.')
                                    
                                    thief.coins += cur_player.coins
                                    
                                    cur_player.coins = 0

                                    robbed_char = ''

                                if selected_chars[char_index] == CHARACTERS[3]:
                                    spec_feat = False
                                    while players_id[0] != player.id:
                                        players_id.append(players_id.pop(0))
                                        players_names.append(players_names.pop(0))
                                        
                                    for pid in players_id+waiters_id:
                                        if pid != cur_player.id:
                                            bot.send_message(pid, player.name +  ' получает корону 👑 и в следующем раунде будет первым выбирать персонажа')
                                        else:
                                            bot.send_message(pid, 'Вы получаете корону 👑 и в следующем раунде будете первым выбирать персонажа')

                                if selected_chars[char_index] == CHARACTERS[5]:
                                    spec_feat = False
                                    cur_player.coins += 1
                                    for _player in Players:
                                        if _player.id != cur_player.id:
                                            bot.send_message(_player.id, player.name +  ' как купец получает одну бонусную монету 🏅')
                                        else:
                                            bot.send_message(_player.id, 'Вы получаете одну бонусную монету 🏅')

                                if (selected_chars[char_index] == CHARACTERS[4] or
                                   (selected_chars[char_index] == CHARACTERS[6])):
                                   spec_feat = False

                                if selected_chars[char_index] == CHARACTERS[6]:
                                    taken_quarts = []
                                    
                                    for i in range(2):
                                        t_quart = ran.choice(q.quarts)
                                        q.quarts.remove(t_quart)
                                        cur_player.quarts.append(t_quart)
                                        taken_quarts.append(t_quart)

                                    for _player in players_id+waiters_id:
                                        if _player == cur_player.id:
                                            bot.send_message(_player, 'Как зодчий Вы получаете две доп. карты:\n\n'+'\n\n'.join(map(str,taken_quarts)))
                                        else:
                                            bot.send_message(_player, cur_player.name+' как зодчий получает две доп. карты кварталов')

                                if ((selected_chars[char_index] == CHARACTERS[3]) or
                                    (selected_chars[char_index] == CHARACTERS[4]) or 
                                    (selected_chars[char_index] == CHARACTERS[5]) or
                                    (selected_chars[char_index] == CHARACTERS[7])):
                                    
                                    collect_coins = True 
                               
                                else:
                                    collect_coins = False
                                    
                                lab = False    
                                if q.lab in cur_player.b_quarts:
                                    lab = True

                                smithy = False
                                if q.smithy in cur_player.b_quarts and (cur_player.coins >= 2):
                                    smithy = True

                                enough_coins = False
                                for quart in cur_player.quarts:
                                    if cur_player.coins >= quart.cost and (quart not in cur_player.b_quarts):
                                        enough_coins = True
                                        break

                                reload_play_keyboard()

                                bot.send_message(player.id, 'Ваш ход. Нажмите на кнопку, чтобы выполнить действие', reply_markup = keyboard9)
                                
                                moves_start = False  

                                break  

  mes_sync = True


try:                                        
    bot.polling(none_stop=True, interval=0)
except requests.exceptions.ReadTimeout:
    print("Переподключение к серверам\n")
    bot.polling(none_stop=True, interval=0)
