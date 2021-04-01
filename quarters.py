class Quart:
    def __init__(self, type, name, cost, desc=''):
        self.type = type
        self.name = name
        self.cost = cost
        self.desc = desc
    
    def __str__(self):
        if self.desc == '':
            return self.type+self.name+self.cost*'🏅'
        else:
            return self.type+self.name+self.cost*'🏅'+':\n'+self.desc
     
palazzo = Quart('🟡', 'Палаццо', 5,'')
castle = Quart('🟡', 'Замок', 4,'')
port = Quart('🟢', 'Порт', 3,'')
market = Quart('🟢', 'Рынок', 2, '')
tavern = Quart('🟢', 'Таверна',1 , '')
shop = Quart('🟢', 'Лавка',2 , '')
town_hall = Quart('🟢', 'Ратуша',5 , '')
harbor = Quart('🟢', 'Гавань', 4 , '')
estate = Quart('🟡', 'Поместье',3 , '')
mars_field = Quart('🔴', 'Марсово поле',3 , '')
prison = Quart('🔴', 'Тюрьма',3 , '')
watchtower = Quart('🔴', 'Дозорная башня',1 , '')
fortress = Quart('🔴', 'Крепость',5 , '')
monastery = Quart('🔵', 'Монастырь', 3, '')
temple = Quart('🔵', 'Храм',1 , '')
church = Quart('🔵', 'Церковь',2 , '')
cathedral = Quart('🔵', 'Собор',5 , '')
dragon_gates = Quart('🟣', 'Врата дракона', 6, 'в конце игры получаете 2 доп.очка')
great_wall = Quart('🟣', 'Великая стена',6 , 'чтобы разрушить любой другой из ваших кварталов, кондотьер должен заплатить в банк на 1 золотой больше')
lab = Quart('🟣', 'Лаборатория',5 , 'раз в свой ход вы можете сбросить карту квартала с руки и получить 2 золотых из банка')
hogwarts = Quart('🟣', 'Школа магии',6 , 'когда вы применяете свойства, позволяющие получить ресурсы за кварталы, школа магии считается кварталом вашего типа')
lib = Quart('🟣', 'Библиотека',6 , 'если вы решаете при сборе ресурсов тянуть карты, оставьте на руке все вытянутые карты')
fort = Quart('🟣', 'Форт',3 , 'кондотьер не может разрушить форт')
smithy = Quart('🟣', 'Кузня', 5, 'раз в свой ход вы можете заплатить 2 золотых в банк, чтобы взять из колоды на руку 3 карты кварталов')
observ = Quart('🟣', 'Обсерватория',4 , 'если вы решаете при сборе ресурсов тянуть карты, тяните 3 вместо 2')
grave = Quart('🟣', 'Кладбище',5 , 'когда кондотьер разрушает квартал любого игрока, вы можете заплатить в банк 1 золотой, чтобы забрать разрушенный квартал на руку')
univer = Quart('🟣', 'Университет',6 , 'в конце игры получаете 2 доп. очка')
coffers = Quart('🟣', 'Имперская казна',5 , 'в конце игры получите 1 дополнительное очко за каждый золотой в вашем распоряжении')
ghost = Quart('🟣', 'Квартал призраков',2 , 'если в конце вам не будет хватать только одного типа кварталов, то квартал призраков засчитывается за недостающий тип')
assem = Quart('🟣', 'Собрание карт', 5, 'в конце игры получите 1 дополнительное очко за каждую карту у вас на руке')

QUARTS = [palazzo, palazzo, palazzo, castle, castle, castle, castle, port, port, port, market, market, tavern, tavern, tavern, tavern, market, market, shop, shop, shop, town_hall, town_hall, harbor, harbor, harbor, estate, estate, estate, estate, estate, mars_field, mars_field, mars_field, fortress, fortress, prison, prison, prison,  watchtower, watchtower, watchtower, watchtower,  temple, temple, temple,temple, monastery, monastery, monastery, great_wall, cathedral, cathedral, church, church, church, lab, hogwarts, lib, fort, univer, smithy, coffers, observ, ghost, assem, grave, dragon_gates]

#QUARTS = [lab, hogwarts, lib, fort, univer, smithy, coffers, observ, ghost, assem, grave, dragon_gates]


quarts = []

for quart in QUARTS:
    quarts.append(quart)

quarts_names = []

for quart in QUARTS:
    quarts_names.append(quart.name)
    
