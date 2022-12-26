import telebot, wikipedia, random, datetime, sqlite3
from googlesearch import search
import numpy as np


bot = telebot.TeleBot('5740263278:AAFTyI5d5q5DyT5SwiH6yfGOQHKeazR26EU')
namebot = 'Ева'
wikipedia.set_lang('ru')
date_and_time = datetime.datetime.now().strftime('%H.%M.%S : %d-%m-%Y')
conn = sqlite3.connect('db/evadatabase.db', check_same_thread=False)
cursor = conn.cursor()
registration = []


@bot.message_handler(content_types=['text'])
def communication(message):
    result = message.text
    if result.startswith("Ева ищи"):
        bot.send_message(message.chat.id, 'Ищу...')
        for link in search(result, tld='co.in', num=5, stop=5, pause=2):
            bot.send_message(message.chat.id, link)
    elif result == 'Ева':
        answer_list = ['Ай?', 'Я тут', 'Что случилось?', 'Чем я могу помочь?', 'Слушаю', 'Да?',
                       'Что Вас интересует?']
        answer = random.choice(answer_list)
        bot.send_message(message.chat.id, answer)
    elif result == 'Ева дата' or result == 'Ева время' or result == 'Ева, дата' or result == 'Ева, время':
        bot.send_message(message.chat.id, date_and_time)
    for_choise = str(result).split(' ')
    if len(for_choise) >= 3:
        if for_choise[0] == 'Ева' and for_choise[2] == 'или':
            list_choise = [for_choise[1], for_choise[3]]
            bot.send_message(message.chat.id, f'Я считаю, что лучше {random.choice(list_choise)}')
    elif result == 'Ева молодец' or result == 'Ева, молодец':
        bot.send_message(message.chat.id, 'Спасибо, мне очень приятно :)')
    if result == '/All@EvavaFamilyBot' or result == '/All':
        bot.send_message(message.chat.id, 'Вот вся база данных:\n'
                                          'Порядковый номер, id телеграмм, имя, дата рождения.')
        a = cursor.execute(f'SELECT * FROM evabase').fetchall()
        b = []
        for i in a:
            b.append(i)
        bot.send_message(message.chat.id, f'{np.array(b)}')
        b.clear()
    elif result == '/Add_my_event@EvavaFamilyBot' or result == '/Add_my_event':
        bot.send_message(message.chat.id, 'Введите название события, и дату события, чтобы добавить его.'
                                          'ВНИМАНИЕ‼️\nСначала введите событие, потом "!" после чего дату '
                                          '(в формате ГГГГ-ММ-ДД)'
                                          '. В одну строчку.\nПример: Событие ! дата')

    elif result == '/My_event@EvavaFamilyBot' or result == '/My_event':
        us_id = message.from_user.id
        c = cursor.execute(f'SELECT event, event_date FROM events WHERE user_id = {us_id}').fetchall()
        cc = []
        for jj in c:
            cc.append(jj)
        bot.send_message(message.chat.id, f'Ваши текущие события:\n{np.array(cc)}\n\n\n'
                                          f'Добавить новые события можно через меню /base '
                                          f'или команду /Add_my_event\n'
                                          f'Удалить все события можно командой /Delete_my_event')
        cc.clear()
    elif result == '/Delete_my_event@EvavaFamilyBot' or result == '/Delete_my_event':
        us_id = message.from_user.id
        d = cursor.execute(f'SELECT event, event_date FROM events WHERE user_id = {us_id}').fetchall()
        dd = []
        for jjj in d:
            dd.append(jjj)
        bot.send_message(message.chat.id, f'Вы действительно хотите удалить все события?\n'
                                          f'Ответьте: Да/Нет\n\n\n'
                                          f'{np.array(dd)}')

        dd.clear()
    elif result == '/Show_all_event@EvavaFamilyBot' or result == '/Show_all_event':
        try:
            e = cursor.execute(f'SELECT * FROM all_events').fetchall()
            ee = []
            for kk in e:
                ee.append(kk)
            bot.send_message(message.chat.id, f'Текущие общие события:\n{np.array(ee)}\n\n\n'
                                              f'Добавить новые события можно через меню /base '
                                              f'или команду /Add_all_event')
            ee.clear()
        except Exception as error:
            bot.send_message(message.chat.id, 'Произошла неизвестная ошибка. Попробуйте еще раз.')
    elif result == '/Add_all_event@EvavaFamilyBot' or result == '/Add_all_event':
        bot.send_message(message.chat.id, 'Введите название события, и дату события, чтобы добавить его.'
                                          'ВНИМАНИЕ‼️\nСначала введите событие, потом "!" после чего дату(в формате '
                                          'ГГГГ-ММ-ДД '
                                          '. В одну строчку.\nПример: Событие ! дата')

    elif result == '/Delete_all_event@EvavaFamilyBot' or result == '/Delete_all_event':
        events = cursor.execute(f'SELECT * FROM all_events').fetchall()
        eee = []
        for kkk in events:
            eee.append(kkk)
        bot.send_message(message.chat.id, f'Текущие общие события:\n{np.array(eee)}\n\n\n'
                                          f'Выберите номер события, которое хотите удалить.')
        eee.clear()


bot.infinity_polling()
