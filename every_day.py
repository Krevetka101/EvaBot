# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot, wikipedia, datetime, sqlite3, requests, random
import numpy as np
from bs4 import BeautifulSoup

bot = telebot.TeleBot('5740263278:AAFTyI5d5q5DyT5SwiH6yfGOQHKeazR26EU')
namebot = 'Ева'
wikipedia.set_lang('ru')
today_date = datetime.date.today()
date_and_time = datetime.datetime.now().strftime('%H.%M.%S : %d-%m-%Y')
conn = sqlite3.connect('db/evadatabase.db', check_same_thread=False)
cursor = conn.cursor()
holidays = []
result_holidays = ''


# Отсчет дней
def count_day(dat):
    try:
        current_date = str(datetime.date.today()).split('-')
        date_bd = str(dat).split('-')
        count_now = 0
        count_bd = 0
        year_now = current_date[0].strip()
        year_bd = date_bd[0].strip()
        month_now = current_date[1].strip()
        month_bd = date_bd[1].strip()
        day_now = current_date[2].strip()
        day_bd = date_bd[2].strip()
        if year_now == year_bd:
            if month_now == month_bd:
                if day_now == day_bd:
                    return 'Уже сегодня! 🎂'
                elif day_now < day_bd:
                    count_now = int(day_now)
                    count_bd = int(day_bd)
                    ret = f'Осталось {count_bd - count_now} дня/дней'
                    return ret
                elif day_now > day_bd:
                    return 'Событие уже прошло! 😞'
            elif month_now > month_bd:
                return 'Событие уже прошло! 😞'
            elif month_now < month_bd:
                ret = f'В следующем месяце'
                return ret
        elif year_now > year_bd:
            return 'Событие уже прошло! 😞'
        elif year_now < year_bd:
            return 'Еще не скоро!'
    except Exception:
        return 'Дата не поддерживается 🫠'


# Рассылка
results = cursor.execute('SELECT chat_id FROM chats_id').fetchall()
total_results = []

# Праздники
url = 'https://my-calend.ru/holidays'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'lxml')
temp = bs.find(class_='holidays-items')
for item in temp:
    holidays.append(item.text)
temp2 = bs.find(class_='holidays-name-days')
for check in holidays:
    word = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
            'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё',
            'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ',
            'Ы', 'Ь', 'Э', 'Ю', 'Я']
    if len(check) > 3:
        for double_check in check:
            if double_check in word:
                result_holidays += double_check
            elif double_check == ' ':
                result_holidays += ' '
        result_holidays += '\n'


# Погода
def weather(city):
    fin_city = ''
    cit = np.array(city)
    for wwwa in cit:
        fin_city += wwwa
    fin_city = str(fin_city).replace('_', '/')
    weather_result = ''
    url_weather = f'https://world-weather.ru/pogoda/{fin_city}/'
    response2 = requests.get(url_weather)
    bs2 = BeautifulSoup(response2.text, 'lxml')
    temp_weather = bs2.find(id="defSet-2")
    finish = str(temp_weather.text)
    count = 0
    for check_words in finish:
        words = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
                 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        if count < 5:
            if check_words in words:
                if count < 4:
                    weather_result += '\n' + check_words
                count += 1
            else:
                weather_result += check_words
    return weather_result


# Гороскоп
# Овен
def oven():
    url_goroskop_oven = 'https://horo.mail.ru/prediction/aries/today/'
    response_oven = requests.get(url_goroskop_oven)
    bs_oven = BeautifulSoup(response_oven.text, 'lxml')
    oven = bs_oven.find(class_='article__text')
    return oven.text


# Телец
def telec():
    url_goroskop_telec = 'https://horo.mail.ru/prediction/taurus/today/'
    response_telec = requests.get(url_goroskop_telec)
    bs_telec = BeautifulSoup(response_telec.text, 'lxml')
    telec = bs_telec.find(class_='article__text')
    return telec.text


# Близнецы
def blizn():
    url_goroskop_blizn = 'https://horo.mail.ru/prediction/gemini/today/'
    response_blizn = requests.get(url_goroskop_blizn)
    bs_blizn = BeautifulSoup(response_blizn.text, 'lxml')
    blizn = bs_blizn.find(class_='article__text')
    return blizn.text


# Рак
def rak():
    url_goroskop_rak = 'https://horo.mail.ru/prediction/cancer/today/'
    response_rak = requests.get(url_goroskop_rak)
    bs_rak = BeautifulSoup(response_rak.text, 'lxml')
    rak = bs_rak.find(class_='article__text')
    return rak.text


# Лев
def lev():
    url_goroskop_lev = 'https://horo.mail.ru/prediction/leo/today/'
    response_lev = requests.get(url_goroskop_lev)
    bs_lev = BeautifulSoup(response_lev.text, 'lxml')
    lev = bs_lev.find(class_='article__text')
    return lev.text


# Дева
def deva():
    url_goroskop_deva = 'https://horo.mail.ru/prediction/virgo/today/'
    response_deva = requests.get(url_goroskop_deva)
    bs_deva = BeautifulSoup(response_deva.text, 'lxml')
    deva = bs_deva.find(class_='article__text')
    return deva.text


# Весы
def vesi():
    url_goroskop_vesi = 'https://horo.mail.ru/prediction/libra/today/'
    response_vesi = requests.get(url_goroskop_vesi)
    bs_vesi = BeautifulSoup(response_vesi.text, 'lxml')
    vesi = bs_vesi.find(class_='article__text')
    return vesi.text


# Скорпион
def scorpion():
    url_goroskop_scorp = 'https://horo.mail.ru/prediction/scorpio/today/'
    response_scorp = requests.get(url_goroskop_scorp)
    bs_scorp = BeautifulSoup(response_scorp.text, 'lxml')
    scorp = bs_scorp.find(class_='article__text')
    return scorp.text


# Стрелец
def strelec():
    url_goroskop_strel = 'https://horo.mail.ru/prediction/sagittarius/today/'
    response_strel = requests.get(url_goroskop_strel)
    bs_strel = BeautifulSoup(response_strel.text, 'lxml')
    strel = bs_strel.find(class_='article__text')
    return strel.text


# Козерог
def kozerog():
    url_goroskop_koz = 'https://horo.mail.ru/prediction/capricorn/today/'
    response_koz = requests.get(url_goroskop_koz)
    bs_koz = BeautifulSoup(response_koz.text, 'lxml')
    koz = bs_koz.find(class_='article__text')
    return koz.text


# Водолей
def vodoley():
    url_goroskop_vodol = 'https://horo.mail.ru/prediction/aquarius/today/'
    response_vodol = requests.get(url_goroskop_vodol)
    bs_vodol = BeautifulSoup(response_vodol.text, 'lxml')
    vodol = bs_vodol.find(class_='article__text')
    return vodol.text


# Рыбы
def ribi():
    url_goroskop_fish = 'https://horo.mail.ru/prediction/pisces/today/'
    response_fish = requests.get(url_goroskop_fish)
    bs_fish = BeautifulSoup(response_fish.text, 'lxml')
    fish = bs_fish.find(class_='article__text')
    return fish.text


# Сообщения бота
morning_cartoon = ['💐', '🌷', '🌹', '🪷', '🌺', '🌸', '🌼', '🌻']
result_morning_cartoon = random.choice(morning_cartoon)
for aa in results:
    np.array(aa)
    total_results.append(aa)
for messages in total_results:
    a = cursor.execute(f'SELECT id, user_name, event, date '
                       f'FROM evabase WHERE chat_id= {messages[0]}').fetchall()
    aa = []
    for recurse in a:
        aa.append(recurse)
    bb = np.array(aa)
    result_events = ''
    for res_ev in bb:
        check_days = count_day(res_ev[3])
        result_events += str(res_ev[0]) + ' ' + str(res_ev[1]) + ' ' + str(res_ev[2]) + \
                         ' ' + str(res_ev[3]) + ' | ' + str(check_days) + '\n'
    check_events = result_events
    if temp2 is None:
        bot.send_message(messages[0], f'<b>Доброе утро!</b>{result_morning_cartoon}\n'
                                      f'<b>Сегодня:</b> {today_date}\n'
                                      f'<b>Сегодняшние праздники:</b>🎂\n'
                                      f'{result_holidays}\n', parse_mode='html')
    else:
        bot.send_message(messages[0], f'<b>Доброе утро!</b>{result_morning_cartoon}\n'
                                      f'<b>Сегодня:</b> {today_date}\n'
                                      f'<b>Сегодняшние праздники:</b>🎂\n'
                                      f'{result_holidays}'
                                      f'\n{temp2.text}\n', parse_mode='html')
    try:
        awggawawg = cursor.execute(f'SELECT city FROM chats_id WHERE chat_id ={messages[0]}').fetchone()
        check_awg = np.array(awggawawg)
        hggg = weather(awggawawg)
        bot.send_message(messages[0], f'<b>Погода на сегодня в {check_awg}:</b>🌅\n{hggg}\n'
                                      f'Чтобы изменить страну/город напишите "Сменить город"',
                         parse_mode='html')
    except Exception:
        bot.send_message(messages[0], 'Выбранный Вами город не найден, попробуйте сменить его '
                                      'написав <b>Сменить город</b>', parse_mode='html')
    pull_goro = cursor.execute(f'SELECT goro FROM chats_id WHERE chat_id={messages[0]}').fetchall()
    finish_goro = np.array(pull_goro)
    goroscop = ''
    goroscop2 = ''
    for check_goro in finish_goro[0]:
        two = str(check_goro).split(',')
        for _ in range(len(two)):
            if 'oven' in two:
                goroscop += 'Овен:♈' + '\n' + oven() + '\n'
                two.remove('oven')
            elif 'telec' in two:
                goroscop += 'Телец:♉' + '\n' + telec() + '\n'
                two.remove('telec')
            elif 'blizn' in two:
                goroscop += 'Близнецы:♊' + '\n' + blizn() + '\n'
                two.remove('blizn')
            elif 'rak' in two:
                goroscop += 'Рак:♋' + '\n' + rak() + '\n'
                two.remove('rak')
            elif 'lev' in two:
                goroscop += 'Лев:♌' + '\n' + lev() + '\n'
                two.remove('lev')
            elif 'deva' in two:
                goroscop += 'Дева:♍' + '\n' + deva() + '\n'
                two.remove('deva')
            elif 'vesi' in two:
                goroscop2 += 'Весы:♎' + '\n' + vesi() + '\n'
                two.remove('vesi')
            elif 'scorpion' in two:
                goroscop2 += 'Скорпион:♏' + '\n' + scorpion() + '\n'
                two.remove('scorpion')
            elif 'strelec' in two:
                goroscop2 += 'Стрелец:♐' + '\n' + strelec() + '\n'
                two.remove('strelec')
            elif 'kozerog' in two:
                goroscop2 += 'Козерог:♑' + '\n' + kozerog() + '\n'
                two.remove('kozerog')
            elif 'vodoley' in two:
                goroscop2 += 'Водолей:♒' + '\n' + vodoley() + '\n'
                two.remove('vodoley')
            elif 'ribi' in two:
                goroscop2 += 'Рыбы:♓' + '\n' + ribi() + '\n'
                two.remove('ribi')
            elif check_goro == 'vse':
                goroscop += 'Овен:♈' + '\n' + oven() + '\n' + 'Телец:♉' + '\n' + telec() + '\n' + 'Близнецы:♊' + '\n' + blizn() + '\n' + 'Рак:♋' + '\n' + rak() + '\n' + 'Лев:♌' + '\n' + lev() + '\n' + 'Дева:♍' + '\n' + deva() + '\n'
                goroscop2 += 'Весы:♎' + '\n' + vesi() + '\n' + 'Скорпион:♏' + '\n' + scorpion() + '\n' + 'Стрелец:♐' + '\n' + strelec() + '\n' + 'Козерог:♑' + '\n' + kozerog() + '\n' + 'Водолей:♒' + '\n' + vodoley() + '\n' + 'Рыбы:♓' + '\n' + ribi() + '\n '
    if goroscop != '' and goroscop2 != '':
        bot.send_message(messages[0], f'<b>Гороскоп на сегодня:</b>🌠\n'
                                      f'{goroscop}', parse_mode='html')
        bot.send_message(messages[0], f'\n{goroscop2}\nДля выбора знаков зодиака '
                                      f'напишите <b>Выбрать знаки</b>', parse_mode='html')
    elif goroscop != '':
        bot.send_message(messages[0], f'<b>Гороскоп на сегодня:</b>🌠\n'
                                      f'{goroscop}\nДля выбора знаков зодиака '
                                      f'напишите <b>Выбрать знаки</b>', parse_mode='html')
    elif goroscop2 != '':
        bot.send_message(messages[0], f'<b>Гороскоп на сегодня:</b>🌠\n'
                                      f'{goroscop2}\nДля выбора знаков зодиака '
                                      f'напишите <b>Выбрать знаки</b>', parse_mode='html')
    # bot.send_message(messages[0], f'<b>Гороскоп на сегодня:</b>🌠\n'
    #                               f'<b>Овен:</b>♈️\n{oven.text}\n'
    #                               f'<b>Телец:</b>♉️\n{telec.text}\n'
    #                               f'<b>Близнецы:</b>♊️\n{blizn.text}\n'
    #                               f'<b>Рак:</b>♋️\n{rak.text}\n'
    #                               f'<b>Лев:</b>♌️\n{lev.text}\n'
    #                               f'<b>Дева:</b>♍️\n{deva.text}\n', parse_mode='html')
    # bot.send_message(messages[0], f'<b>Весы:</b>♎️\n{vesi.text}\n'
    #                               f'<b>Скорпион:</b>♏️\n{scorp.text}\n'
    #                               f'<b>Стрелец:</b>♐️\n{strel.text}\n'
    #                               f'<b>Козерог:</b>♑️\n{koz.text}\n'
    #                               f'<b>Водолей:</b>♒️\n{vodol.text}\n'
    #                               f'<b>Рыбы:</b>♓️\n{fish.text}\n', parse_mode='html')
    check_events_two = check_events.replace(' ', '')
    if check_events_two != '':
        bot.send_message(messages[0], '<b>События в Вашем чате:</b>\n'
                                      '<b>ID события:</b>  <b>Кто создал событие:</b>  '
                                      '<b>Текст события:</b>  <b>Дата события:</b>\n'
                                      f'{result_events}', parse_mode='html')
    else:
        bot.send_message(messages[0], 'События в Вашем чате еще не созданы.\n'
                                      'Для их создания напишите <b>Ева, события</b>', parse_mode='html')
total_results.clear()
