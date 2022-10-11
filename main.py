import telebot, wikipedia, random, datetime, schedule, asyncio, sqlite3
from googlesearch import search
import numpy as np


def main():
    bot = telebot.TeleBot('5740263278:AAFTyI5d5q5DyT5SwiH6yfGOQHKeazR26EU')
    namebot = 'Ева'
    wikipedia.set_lang('ru')
    date_and_time = datetime.datetime.now().strftime('%H.%M.%S : %d-%m-%Y')
    conn = sqlite3.connect('db/evadatabase.db', check_same_thread=False)
    cursor = conn.cursor()
    registration = []

    def db_table_val(user_id: int, user_name: str, birthday: str):
        cursor.execute('INSERT INTO evabase (user_id, user_name, birthday) VALUES(?, ?, ?)',
                       (user_id, user_name, birthday))
        conn.commit()

    def new_event(user_id: int, event: str, event_date: str):
        cursor.execute('INSERT INTO events (user_id, event, event_date) VALUES(?, ?, ?)', (user_id, event, event_date))
        conn.commit()

    def all_new_event(event: str, date: str):
        cursor.execute('INSERT INTO all_events (event, date) VALUES(?, ?)', (event, date))
        conn.commit()

    @bot.message_handler(commands=['reg'])
    def register(message):
        bot.reply_to(message, 'Введите Ваше имя')
        bot.register_next_step_handler(message, register_2)

    def register_2(message):
        registration.append(message.text)
        bot.reply_to(message, 'Введите дату рождения, в формате ГГГГ-ММ-ДД. Знак "-" обязателен.‼️')
        bot.register_next_step_handler(message, register_3)

    def register_3(message):
        registration.append(message.text)
        bot.reply_to(message, f'Всё верно?\n{registration[0]}\n{registration[1]}')
        bot.register_next_step_handler(message, register_4)

    def register_4(message):
        try:
            answer = message.text
            if answer == 'Да' or answer == 'да':
                bot.reply_to(message, 'Отлично. Данные внесены в базу данных ✅\nСпасибо!\n'
                                      'Теперь вы можете добавлять и просмотривать события.\n'
                                      'Для этого нужно ввести /base')
                us_id = message.from_user.id
                us_name = registration[0]
                birth = registration[1]
                db_table_val(user_id=us_id, user_name=us_name, birthday=birth)
                registration.clear()
            elif answer == 'Нет' or answer == 'нет':
                registration.clear()
                bot.reply_to(message, 'Тогда, давайте начнем все сначала. Введите /reg')
        except Exception as error:
            registration.clear()
            bot.reply_to(message, 'Ошибка. Скорее всего, вы уже есть в базе.')

    @bot.message_handler(commands=['base'])
    def base_req(message):
        bot.reply_to(message, 'Выберите действие с базой данных:\n'
                              '/All - Вся база📖\n'
                              '/My_event - Ваши события📖\n'
                              '/Add_my_event - Добавить мое событие🖌\n'
                              '/Add_all_event - Добавить общее событие🖌\n'
                              '/Show_all_event - Показать общие события📖\n'
                              '/Delete_my_event - Удалить все Ваши события🖍\n'
                              '/Delete_all_event - Удалить общее событие🖍')

    @bot.message_handler(commands=['help'])
    def send_comands(message):
        bot.reply_to(message, 'Вот что я умею:\n'
                              '📔Для поиска слов в Wikipedia, введите /Найди (объект)\n'
                              '🌐Для поиска в интернете, введите Ева ищи\n'
                              '📅Для просмотра времени и даты напишите Ева, дата или Ева, время\n'
                              'Вы так же, всегда можете узнать моё мнение, для этого нужно '
                              'написать Ева 1 или 2\n'
                              '🗂Для управления событиями, введите команду /base')

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Добрый день. Меня зовут Ева. Я семейный чат-бот👋\n"
                              "Список моих возможностей можно посмотреть командой /help\n"
                              "Вы всегда можете ко мне обратиться, всегда готова помочь.\n"
                              "И меня всегда можно похвалить. Мне будет приятно 😋\n"
                              "Возможны временные сбои в моей работе, но я пока только учусь.")
        bot.reply_to(message, 'Для начала, давайте познакомимся. Введите /reg чтобы начать небольшую регистрацию📝')

    def wikisearch(word):
        try:
            result = wikipedia.summary(word)
            return result
        except Exception as e:
            return 'В энциклопедии нет информации об этом'

    @bot.message_handler(commands=['Найди'], content_types=['text'])
    def searchwiki(message):
        bot.reply_to(message, 'Начинаю поиск')
        word = str(message).lower().split(' ')
        bot.send_message(message.chat.id, wikisearch(word))

    @bot.message_handler(content_types=['text'])
    def communication(message):
        result = message.text
        if result.startswith("Ева ищи"):
            bot.reply_to(message, 'Ищу...')
            for link in search(result, tld='co.in', num=5, stop=5, pause=2):
                bot.reply_to(message, link)
        elif result == 'Ева':
            answer_list = ['Ай?', 'Я тут', 'Что случилось?', 'Чем я могу помочь?', 'Слушаю', 'Да?',
                           'Что Вас интересует?']
            answer = random.choice(answer_list)
            bot.reply_to(message, answer)
        elif result == 'Ева дата' or result == 'Ева время' or result == 'Ева, дата' or result == 'Ева, время':
            bot.reply_to(message, date_and_time)
        for_choise = str(result).split(' ')
        if len(for_choise) >= 3:
            if for_choise[0] == 'Ева' and for_choise[2] == 'или':
                list_choise = [for_choise[1], for_choise[3]]
                bot.reply_to(message, f'Я считаю, что лучше {random.choice(list_choise)}')
        elif result == 'Ева молодец' or result == 'Ева, молодец':
            bot.reply_to(message, 'Спасибо, мне очень приятно :)')
        if result == '/All@EvavaFamilyBot' or result == '/All':
            bot.reply_to(message, 'Вот вся база данных:\n'
                                  'Порядковый номер, id телеграмм, имя, дата рождения.')
            a = cursor.execute(f'SELECT * FROM evabase').fetchall()
            b = []
            for i in a:
                b.append(i)
            bot.reply_to(message, f'{np.array(b)}')
            b.clear()
        elif result == '/Add_my_event@EvavaFamilyBot' or result == '/Add_my_event':
            bot.reply_to(message, 'Введите название события, и дату события, чтобы добавить его.'
                                  'ВНИМАНИЕ‼️\nСначала введите событие, потом "!" после чего дату '
                                  '(в формате ГГГГ-ММ-ДД)'
                                  '. В одну строчку.\nПример: Событие ! дата')
            bot.register_next_step_handler(message, add_new_event)
        elif result == '/My_event@EvavaFamilyBot' or result == '/My_event':
            us_id = message.from_user.id
            c = cursor.execute(f'SELECT event, event_date FROM events WHERE user_id = {us_id}').fetchall()
            cc = []
            for jj in c:
                cc.append(jj)
            bot.reply_to(message, f'Ваши текущие события:\n{np.array(cc)}\n\n\n'
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
            bot.reply_to(message, f'Вы действительно хотите удалить все события?\n'
                                  f'Ответьте: Да/Нет\n\n\n'
                                  f'{np.array(dd)}')
            bot.register_next_step_handler(message, delete_event)
            dd.clear()
        elif result == '/Show_all_event@EvavaFamilyBot' or result == '/Show_all_event':
            try:
                e = cursor.execute(f'SELECT * FROM all_events').fetchall()
                ee = []
                for kk in e:
                    ee.append(kk)
                bot.reply_to(message, f'Текущие общие события:\n{np.array(ee)}\n\n\n'
                                      f'Добавить новые события можно через меню /base '
                                      f'или команду /Add_all_event')
                ee.clear()
            except Exception as error:
                bot.reply_to(message, 'Произошла неизвестная ошибка. Попробуйте еще раз.')
        elif result == '/Add_all_event@EvavaFamilyBot' or result == '/Add_all_event':
            bot.reply_to(message, 'Введите название события, и дату события, чтобы добавить его.'
                                  'ВНИМАНИЕ‼️\nСначала введите событие, потом "!" после чего дату(в формате ГГГГ-ММ-ДД'
                                  '. В одну строчку.\nПример: Событие ! дата')
            bot.register_next_step_handler(message, add_all_event)
        elif result == '/Delete_all_event@EvavaFamilyBot' or result == '/Delete_all_event':
            events = cursor.execute(f'SELECT * FROM all_events').fetchall()
            eee = []
            for kkk in events:
                eee.append(kkk)
            bot.reply_to(message, f'Текущие общие события:\n{np.array(eee)}\n\n\n'
                                  f'Выберите номер события, которое хотите удалить.')
            eee.clear()
            bot.register_next_step_handler(message, delete_all_events)

    def delete_all_events(message):
        number = int(message.text)
        cursor.execute(f'DELETE FROM all_events WHERE id = "{number}"')
        conn.commit()
        bot.reply_to(message, 'Событие успешно удалено!🖍')

    def add_all_event(message):
        all_add_event = str(message.text).split('!')
        all_new_event(event=all_add_event[0], date=all_add_event[1])
        bot.reply_to(message, 'Событие добавлено✅\n'
                              'Просмотреть общие события можно через меню /base, или команду /Show_all_event\n'
                              'Добавить новое общее событие командой /Add_all_event')

    def delete_event(message):
        us_id = message.from_user.id
        count = message.text
        if count == 'Да' or count == 'да':
            cursor.execute(f'DELETE FROM events '
                           f'WHERE user_id = "{us_id}"')
            conn.commit()
            bot.reply_to(message, 'Ваши события успешно удалены.')
        else:
            bot.reply_to(message, 'Удаление отменено. /My_event')

    def add_new_event(message):
        us_id = message.from_user.id
        new_event_add = str(message.text).split('!')
        new_event(user_id=us_id, event=new_event_add[0], event_date=new_event_add[1])
        bot.reply_to(message, 'Событие добавлено✅\n'
                              'Просмотреть свои события можно через меню /base, или команду /My_event\n'
                              'Добавить новое событие командой /Add_my_event')

    bot.infinity_polling()


if __name__ == '__main__':
    main()
