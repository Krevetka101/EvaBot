import telebot, wikipedia, random, datetime, sqlite3, math
from googlesearch import search
from telebot import types
import numpy as np


def main():
    bot = telebot.TeleBot('5740263278:AAFTyI5d5q5DyT5SwiH6yfGOQHKeazR26EU')
    namebot = 'Ева'
    wikipedia.set_lang('ru')
    date_and_time = datetime.datetime.now().strftime('%H.%M.%S : %d-%m-%Y')
    conn = sqlite3.connect('db/evadatabase.db', check_same_thread=False)
    cursor = conn.cursor()

    def add_chat(chat_id: int):
        cursor.execute('INSERT INTO chats_id (chat_id, events) VALUES(?, ?)', (chat_id, None))
        conn.commit()

    def delete_chat(chat_id):
        cursor.execute(f'DELETE FROM chats_id WHERE chat_id={chat_id}')
        conn.commit()

    def new_event(user_id: int, user_name: str, event: str, date: str, chat_id: str):
        cursor.execute('INSERT INTO evabase (user_id, user_name, event, date, chat_id) '
                       'VALUES(?, ?, ?, ?, ?)', (user_id, user_name, event, date, chat_id))
        conn.commit()

    @bot.message_handler(commands=['help'])
    def send_comands(message):
        bot.send_message(message.chat.id, 'Вот что я умею:\n'
                                          '📔Для поиска слов в Wikipedia, введите <b>/Найди (объект)</b>\n'
                                          '🌐Для поиска в интернете, введите <b>Ева ищи (предмет поиска)</b>\n'
                                          '📅Для просмотра времени и даты напишите <b>Ева, дата</b> '
                                          'или <b>Ева, время</b>\n'
                                          'Вы так же, всегда можете узнать моё мнение, для этого нужно '
                                          'написать <b>Ева (1 вариант) или (2 вариант)</b>\n'
                                          '🗂Для управления событиями, напишите "<b>Ева, события</b>"\n'
                                          '📝Чтобы подключить ежедневные рассылки, напишите "<b>Ева, добавь чат</b>"\n'
                                          'Чтобы выбрать знаки зодиака для гороскопа,'
                                          ' напишите <b>Выбрать знаки</b>\n'
                                          '🏘Чтобы выбрать город для отображения погоды, напишите <b>Сменить город</b>\n'
                                          '📱Встроенный модуль расчета периметра/площади/объема. '
                                          'Для его активации напишите "<b>Ева, математика</b>"\n'
                                          '📨<b>Мой канал, где можно связаться с разработчиком, и узнать '
                                          'новую информацию: @EvaBotSupport </b>', parse_mode='html')

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "<b>Добрый день. Меня зовут Ева. Я чат-бот</b>👋\n"
                                          "Список моих возможностей можно посмотреть командой /help\n"
                                          "У меня есть свой канал, где Вы можете задать вопросы по работе,"
                                          "предложить идею для расширения функционала, и внести "
                                          "пожертвования @EvaBotSupport 🌷\n"
                                          "Возможны временные сбои в моей работе, но я пока только учусь.",
                         parse_mode='html')
        bot.send_message(message.chat.id,
                         'Чтобы подключить ежедневные рассылки, напишите "<b>Ева, добавь чат</b>"📝\n\n'
                         'Туда входят:\n'
                         '<b>Сегодняшние праздники</b>🎂\n'
                         '<b>Прогноз погоды</b>☀️\n'
                         '<b>Гороскопы</b>🌠\n'
                         '<b>События чата</b>📆\n\n'
                         'Чтобы отказаться от рассылок, напишите "Ева, удали чат"\n\n'
                         f'ID Вашего чата: <b>{message.chat.id}</b>', parse_mode='html')

    def wikisearch(word):
        try:
            result = wikipedia.summary(word)
            return result
        except Exception as e:
            return 'В энциклопедии нет информации об этом'

    @bot.message_handler(commands=['Найди'], content_types=['text'])
    def searchwiki(message):
        bot.send_message(message.chat.id, 'Начинаю поиск')
        word = str(message).lower().split(' ')
        bot.send_message(message.chat.id, wikisearch(word))

    def mathem(message):
        kb = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton('Периметр', callback_data='perim')
        kb.add(but1)
        but2 = types.InlineKeyboardButton('Площадь', callback_data='plosh')
        kb.add(but2)
        but3 = types.InlineKeyboardButton('Объем', callback_data='obj')
        kb.add(but3)
        bot.send_message(message.chat.id, 'Что будем считать?', reply_markup=kb)

    def events_chat(message):
        kb = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton('Показать все события', callback_data='show_all')
        kb.add(but1)
        but2 = types.InlineKeyboardButton('Создать событие', callback_data='create_event')
        kb.add(but2)
        but3 = types.InlineKeyboardButton('Удалить событие', callback_data='delete_event')
        kb.add(but3)
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=kb)

    list_goro = []

    def choise_goro(message):
        show_goro = cursor.execute(f'SELECT goro FROM chats_id WHERE chat_id={message.chat.id}').fetchall()
        result_goro = np.array(show_goro)
        kb = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton('Овен', callback_data='oven')
        but2 = types.InlineKeyboardButton('Телец', callback_data='telec')
        but3 = types.InlineKeyboardButton('Близнецы', callback_data='blizn')
        kb.add(but1, but2, but3)
        but4 = types.InlineKeyboardButton('Рак', callback_data='rak')
        but5 = types.InlineKeyboardButton('Лев', callback_data='lev')
        but6 = types.InlineKeyboardButton('Дева', callback_data='deva')
        kb.add(but4, but5, but6)
        but7 = types.InlineKeyboardButton('Весы', callback_data='vesi')
        but8 = types.InlineKeyboardButton('Скорпион', callback_data='scorpion')
        but9 = types.InlineKeyboardButton('Стрелец', callback_data='strelec')
        kb.add(but7, but8, but9)
        but10 = types.InlineKeyboardButton('Козерог', callback_data='kozerog')
        but11 = types.InlineKeyboardButton('Водолей', callback_data='vodoley')
        but12 = types.InlineKeyboardButton('Рыбы', callback_data='ribi')
        kb.add(but10, but11, but12)
        but13 = types.InlineKeyboardButton('Подтвердить', callback_data='accept')
        kb.add(but13)
        bot.send_message(message.chat.id, 'Выберите знаки для гороскопа:\n'
                                          f'Выбранные знаки: <b>{result_goro}</b>', reply_markup=kb, parse_mode='html')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "show_all":
            show_result = cursor.execute(f'SELECT id, user_name, event, date '
                                         f'FROM evabase WHERE chat_id={call.message.chat.id}').fetchall()
            total_show_result = []
            for recurse in show_result:
                total_show_result.append(recurse)
            end_result = np.array(total_show_result)
            result_end = ''
            for res_ev in end_result:
                result_end += str(res_ev[0]) + ' ' + str(res_ev[1]) + ' ' + str(res_ev[2]) + ' ' + str(
                    res_ev[3]) + '\n'
            bot.send_message(chat_id=call.message.chat.id, text=f'Вот Ваши события чата:\n'
                                                                f'<b>ID события:</b>  <b>Кто создал событие:</b>  '
                                                                f'<b>Текст события:</b>  <b>Дата события:</b>\n'
                                                                f'{result_end}', parse_mode='html')
            total_show_result.clear()
        elif call.data == "create_event":
            bot.send_message(call.message.chat.id, 'Введите название события, и дату события, чтобы добавить его.\n'
                                                   '<b>ВНИМАНИЕ</b>‼️\nСначала введите событие, потом "!" после чего '
                                                   'дату '
                                                   '<b>(в формате ГГГГ-ММ-ДД)</b>'
                                                   '. В одну строчку.\n<b>Пример:</b> Событие ! дата',
                             parse_mode='html')
            bot.register_next_step_handler(call.message, add_new_event)
        elif call.data == 'delete_event':
            show_result = cursor.execute(f'SELECT id, user_name, event, date '
                                         f'FROM evabase WHERE chat_id={call.message.chat.id}').fetchall()
            total_show_result = []
            for recurse in show_result:
                total_show_result.append(recurse)
            end_result = np.array(total_show_result)
            result_end = ''
            for res_ev in end_result:
                result_end += str(res_ev[0]) + ' ' + str(res_ev[1]) + ' ' + str(res_ev[2]) + ' ' + str(
                    res_ev[3]) + '\n'
            bot.send_message(chat_id=call.message.chat.id, text=f'Вот Ваши события чата:\n'
                                                                f'<b>ID события:</b>  <b>Кто создал событие:</b>  '
                                                                f'<b>Текст события:</b>  <b>Дата события:</b>\n'
                                                                f'{result_end}\n\n'
                                                                f'Напишите <b>ID</b> события, '
                                                                f'которое хотите удалить', parse_mode='html')
            bot.register_next_step_handler(call.message, delete_event)
        elif call.data == 'perim':
            kb = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton('Квадрат', callback_data='perim_sqare')
            kb.add(but1)
            but2 = types.InlineKeyboardButton('Треугольник', callback_data='perim_treug')
            kb.add(but2)
            but3 = types.InlineKeyboardButton('Круг', callback_data='perim_roll')
            kb.add(but3)
            but4 = types.InlineKeyboardButton('Прямоугольник', callback_data='perim_pryamo')
            kb.add(but4)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text='Выберите фигуру для расчета '
                                                                'периметра:', reply_markup=kb)
        elif call.data == 'perim_sqare':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите сторону <b>квадрата</b>, в <b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, perim_sq)
        elif call.data == 'perim_treug':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите стороны <b>треугольника</b> через запятую '
                                       'в <b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, perim_treug)
        elif call.data == 'perim_roll':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите радиус <b>круга</b> '
                                       'в <b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, perim_roll)
        elif call.data == 'perim_pryamo':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите две стороны <b>прямоугольника</b> '
                                       ' через запятую в <b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, perim_pryamo)
        elif call.data == 'plosh':
            kb = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton('Квадрат', callback_data='plosh_sqare')
            kb.add(but1)
            but2 = types.InlineKeyboardButton('Треугольник', callback_data='plosh_treug')
            kb.add(but2)
            but3 = types.InlineKeyboardButton('Круг', callback_data='plosh_roll')
            kb.add(but3)
            but4 = types.InlineKeyboardButton('Прямоугольник', callback_data='plosh_pryamo')
            kb.add(but4)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text='Выберите фигуру для расчета '
                                                                'площади:', reply_markup=kb)
        elif call.data == 'plosh_sqare':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите сторону <b>квадрата</b> в <b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, plosh_sqare)
        elif call.data == 'plosh_treug':
            kb = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton('Основание и высота', callback_data='plosh_treug_1')
            kb.add(but1)
            but2 = types.InlineKeyboardButton('Две стороны и угол', callback_data='plosh_treug_2')
            kb.add(but2)
            but3 = types.InlineKeyboardButton('Формула Герона', callback_data='plosh_treug_3')
            kb.add(but3)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text='По какой формуле считать?', reply_markup=kb)
        elif call.data == 'plosh_treug_1':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите основание и высоту <b>треугольника</b> в <b>сантиметрах</b>'
                                       'через запятую:', parse_mode='html')
            bot.register_next_step_handler(call.message, plosh_treug_1)
        elif call.data == 'plosh_treug_2':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите две стороны <b>треугольника</b> в <b>сантиметрах</b> '
                                       'и угол в градусах через запятую:', parse_mode='html')
            bot.register_next_step_handler(call.message, plosh_treug_2)
        elif call.data == 'plosh_treug_3':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите три стороны <b>треугольника</b> в '
                                       '<b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, plosh_treug_3)
        elif call.data == 'plosh_roll':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите радиус <b>круга</b> в '
                                       '<b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, plosh_roll)
        elif call.data == 'plosh_pryamo':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите две стороны <b>прямоугольника</b> в '
                                       '<b>сантиметрах</b> через запятую:', parse_mode='html')
            bot.register_next_step_handler(call.message, plosh_pryamo)
        elif call.data == 'obj':
            kb = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton('Куб', callback_data='obj_kub')
            kb.add(but1)
            but2 = types.InlineKeyboardButton('Конус', callback_data='obj_konus')
            kb.add(but2)
            but3 = types.InlineKeyboardButton('Шар', callback_data='obj_roll')
            kb.add(but3)
            but4 = types.InlineKeyboardButton('Параллелепипед', callback_data='obj_parall')
            kb.add(but4)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text='Выберите фигуру для расчета '
                                                                'объема:', reply_markup=kb)
        elif call.data == 'obj_kub':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите сторону <b>куба</b> в '
                                       '<b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, obj_kub)
        elif call.data == 'obj_konus':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите радиус основания <b>конуса</b> и '
                                       'высоту в <b>сантиметрах</b> через запятую:', parse_mode='html')
            bot.register_next_step_handler(call.message, obj_konus)
        elif call.data == 'obj_roll':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите радиус <b>шара</b> в '
                                       '<b>сантиметрах</b>:', parse_mode='html')
            bot.register_next_step_handler(call.message, obj_roll)
        elif call.data == 'obj_parall':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите три ребра <b>параллелепипеда</b> в '
                                       '<b>сантиметрах</b> выходящих из одной вершины:', parse_mode='html')
            bot.register_next_step_handler(call.message, obj_parall)
        elif call.data == 'oven':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Овен удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Овен добавлен в список ✅')
        elif call.data == 'telec':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Телец удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Телец добавлен в список ✅')
        elif call.data == 'blizn':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Близнецы удалены из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Близнецы добавлены в список ✅')
        elif call.data == 'rak':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Рак удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Рак добавлен в список ✅')
        elif call.data == 'lev':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Лев удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Лев добавлен в список ✅')
        elif call.data == 'deva':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Дева удалена из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Дева добавлена в список ✅')
        elif call.data == 'vesi':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Весы удалены из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Весы добавлены в список ✅')
        elif call.data == 'scorpion':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Скорпион удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Скорпион добавлен в список ✅')
        elif call.data == 'strelec':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Стрелец удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Стрелец добавлен в список ✅')
        elif call.data == 'kozerog':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Козерог удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Козерог добавлен в список ✅')
        elif call.data == 'vodoley':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Водолей удален из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Водолей добавлен в список ✅')
        elif call.data == 'ribi':
            if call.data in list_goro:
                list_goro.remove(call.data)
                bot.send_message(call.message.chat.id, 'Рыбы удалены из списка ❌')
            else:
                list_goro.append(call.data)
                bot.send_message(call.message.chat.id, 'Рыбы добавлены в список ✅')
        elif call.data == 'accept':
            push_goro = ''
            for push in list_goro:
                push_goro += push + ','
            cursor.execute(f'UPDATE chats_id SET goro="{push_goro}" WHERE chat_id={call.message.chat.id}')
            conn.commit()
            list_goro.clear()
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, 'Изменения успешно сохранены!')

    def perim_sq(message):
        pre_num = str(message.text).replace(' ', '')
        if pre_num.isdigit():
            num = int(pre_num)
            p = (4 * num).__round__(3)
            bot.send_message(message.chat.id, f'Периметр квадрата со стороной <b>{num}</b> равен:'
                                              f'\n<b>{p} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def perim_treug(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit() and check[2].isdigit():
            if len(check) != 3:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                num3 = int(check[2])
                p = (num1 + num2 + num3).__round__(3)
                bot.send_message(message.chat.id, f'Периметр треугольника со сторонами '
                                                  f'<b>{num1}</b>, <b>{num2}</b> и <b>{num3}</b> '
                                                  f'равен <b>{p} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def perim_roll(message):
        pre_num = str(message.text).replace(' ', '')
        if pre_num.isdigit():
            num = int(pre_num)
            p = (2 * math.pi * num).__round__(3)
            bot.send_message(message.chat.id, f'Периметр круга с радиусом <b>{num}</b> '
                                              f'равен <b>{p} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def perim_pryamo(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit():
            if len(check) != 2:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                p = (2 * (num1 + num2)).__round__(3)
                bot.send_message(message.chat.id, 'Периметр прямоугольника со сторонами '
                                                  f'<b>{num1}</b> и <b>{num2}</b> равен <b>{p} сантиметров</b>',
                                 parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def plosh_sqare(message):
        check = str(message.text).replace(' ', '')
        if check.isdigit():
            num1 = int(check)
            s = (num1 ** 2).__round__(3)
            bot.send_message(message.chat.id, f'Площадь квадрата со сторонами <b>{num1}</b> '
                                              f'равна <b>{s} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def plosh_treug_1(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit():
            if len(check) != 2:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                s = (0.5 * num1 * num2).__round__(3)
                bot.send_message(message.chat.id, f'Площадь треугольника с основанием <b>{num1}</b> '
                                                  f'и высотой <b>{num2}</b> равна <b>{s} сантиметров</b>',
                                 parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def plosh_treug_2(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit() and check[2].isdigit():
            if len(check) != 3:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                num3 = int(check[2])
                s = (0.5 * num1 * num2 * math.sin(num3)).__round__(3)
                bot.send_message(message.chat.id, f'Площадь треугольника со сторонами <b>{num1}</b>'
                                                  f' и <b>{num2}</b> и углом <b>{num3}</b> равна '
                                                  f'<b>{s} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def plosh_treug_3(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit() and check[2].isdigit():
            if len(check) != 3:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                try:
                    num1 = int(check[0])
                    num2 = int(check[1])
                    num3 = int(check[2])
                    p = (num1 + num2 + num3) / 2
                    s = (math.sqrt(p * (p - num1) * (p - num2) * (p - num3))).__round__(3)
                    bot.send_message(message.chat.id, f'Полупериметр треугольника со сторонами <b>{num1}</b>, '
                                                      f'<b>{num2}</b>, и <b>{num3}</b> равен <b>{p} сантиметров</b>\n'
                                                      f'Площадь равна <b>{s} сантиметров</b>', parse_mode='html')
                except Exception:
                    bot.send_message(message.chat.id, 'Получается отрицательное число. Проверьте правильность, '
                                                      'или воспользуйтесь другой формулой.')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def plosh_roll(message):
        check = str(message.text).replace(' ', '')
        if check.isdigit():
            num1 = int(check)
            s = (math.pi * num1 ** 2).__round__(3)
            bot.send_message(message.chat.id, f'Площадь круга с радиусом <b>{num1}</b> '
                                              f'равна <b>{s} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def plosh_pryamo(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit():
            if len(check) != 2:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                s = (num1 * num2).__round__(3)
                bot.send_message(message.chat.id, f'Площадь прямоугольника со '
                                                  f'сторонами <b>{num1}</b> и <b>{num2}</b> равна '
                                                  f'<b>{s} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def obj_kub(message):
        check = str(message.text).replace(' ', '')
        if check.isdigit():
            num1 = int(check)
            v = (num1 ** 3).__round__(3)
            bot.send_message(message.chat.id, f'Объем куба со стороной <b>{num1}</b> '
                                              f'равен <b>{v} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def obj_konus(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit():
            if len(check) != 2:
                bot.send_message(message.chat.id, 'Проверьте правильность написания')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                v = ((1 / 3) * math.pi * num1 ** 2 * num2).__round__(3)
                bot.send_message(message.chat.id, f'Объем конуса с радиусом основания <b>{num1}</b> '
                                                  f'и высотой <b>{num2}</b> равен <b>{v} '
                                                  f'сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def obj_roll(message):
        check = str(message.text).replace(' ', '')
        if check.isdigit():
            num1 = int(check)
            v = ((4 / 3) * math.pi * num1 ** 3).__round__(3)
            bot.send_message(message.chat.id, f'Объем шара с радиусом <b>{num1}</b> '
                                              f'равен <b>{v} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    def obj_parall(message):
        check = str(message.text).replace(' ', '').split(',')
        if check[0].isdigit() and check[1].isdigit() and check[2].isdigit():
            if len(check) != 3:
                bot.send_message(message.chat.id, 'Проверьте правильность ввода')
            else:
                num1 = int(check[0])
                num2 = int(check[1])
                num3 = int(check[2])
                v = (num1 * num2 * num3).__round__(3)
                bot.send_message(message.chat.id, f'Объем параллелепипеда с ребрами '
                                                  f'<b>{num1}, {num2}</b> и <b>{num3}</b> '
                                                  f'равен <b>{v} сантиметров</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Вводить необходимо числа')

    @bot.message_handler(content_types=['text'])
    def communication(message):
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        chat_id = message.chat.id
        result = message.text
        if result.startswith("Ева ищи") or result.startswith('Ева, ищи'):
            bot.send_message(message.chat.id, 'Ищу...')
            for link in search(result[8::], tld='ru', num=5, stop=5, pause=2):
                bot.send_message(message.chat.id, link)
        elif result == 'Ева, события' or result == 'Ева события':
            events_chat(message)
        elif result == 'Ева, добавь чат' or result == 'Ева добавь чат':
            try:
                add_chat(chat_id)
                bot.send_message(message.chat.id, '<b>Готово!</b> Ваш чат успешно добавлен в список рассылок.\n'
                                                  'Теперь каждое утро Вы будете получать информацию <b>о праздниках,'
                                                  ' погоде, и гороскопе, так же, будут отображаться события чата</b>.\n'
                                                  'Добавить события можно написав "Ева, события"\n'
                                                  'По умолчанию погода отображается в Москве. Чтобы изменить город, \n'
                                                  'напишите "<b>Сменить город</b>"\n'
                                                  'Чтобы настроить знаки зодиака для гороскопа напишите '
                                                  '<b>Выбрать знаки</b>', parse_mode='html')
            except Exception:
                bot.send_message(message.chat.id, 'Ваш чат уже добавлен в список рассылок')
        elif result == 'Ева, удали чат' or result == 'Ева удали чат':
            try:
                delete_chat(chat_id)
                bot.send_message(message.chat.id, 'Ваш чат отключен от рассылок')
            except Exception:
                bot.send_message(message.chat.id, 'Вашего чата нет в списке. Возможно, вы его не добавляли')
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
        elif result == 'Ева математика' or result == 'Ева, математика':
            mathem(message)
        elif result == 'Ева, стата' and message.chat.id == 2078991528:
            abc = cursor.execute('SELECT * FROM evabase').fetchall()
            bot.send_message(message.chat.id, 'БД:\n'
                                              f'{np.array(abc)}')
            deg = cursor.execute('SELECT * FROM chats_id').fetchall()
            bot.send_message(message.chat.id, 'События:\n'
                                              f'{np.array(deg)}')
        elif result == 'Сменить город':
            bot.send_message(message.chat.id, 'Введите <b>страну и город '
                                              'на английском языке через /</b>\n'
                                              'Пример:\n'
                                              'Russia/Moscow\n'
                                              'Для предотвращения ошибок воспользуйтесь переводчиком',
                             parse_mode='html')
            bot.register_next_step_handler(message, add_city_db)
        elif result == 'Выбрать знаки' or result == 'выбрать знаки':
            choise_goro(message)

    def add_city_db(message):
        add_city = str(message.text).lower().replace(' ', '')
        finish_city = add_city.replace('/', '_')
        try:
            cursor.execute(f'UPDATE chats_id SET city="{finish_city}" WHERE chat_id={message.chat.id}')
            conn.commit()
            bot.send_message(message.chat.id, f'Город успешно изменен! Погода будет '
                                              f'отображаться в <b>{add_city}</b>', parse_mode='html')
        except Exception:
            bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность ввода')

    def delete_event(message):
        try:
            cursor.execute(f'DELETE FROM evabase WHERE id= {message.text} AND chat_id= {message.chat.id}')
            conn.commit()
            bot.send_message(message.chat.id, 'Ваше событие удалено')
        except Exception:
            bot.send_message(message.chat.id, 'Произошла ошибка\n'
                                              'Проверьте правильность введения <b>ID</b>', parse_mode='html')

    def add_new_event(message):
        try:
            us_id = message.from_user.id
            new_event_add = str(message.text).split('!')
            new_event(user_id=us_id, user_name=message.from_user.first_name,
                      event=new_event_add[0], date=new_event_add[1], chat_id=message.chat.id)
            bot.send_message(message.chat.id, '<b>Событие добавлено</b>✅', parse_mode='html')
        except Exception:
            bot.send_message(message.chat.id, '<b>Ошибка!</b>\n'
                                              'Возможно, отсутствует знак "!"', parse_mode='html')

    bot.infinity_polling()


if __name__ == '__main__':
    main()
