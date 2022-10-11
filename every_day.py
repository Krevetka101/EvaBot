# import telebot, schedule, datetime, time, asyncio
#
# bot2 = telebot.TeleBot('5740263278:AAFTyI5d5q5DyT5SwiH6yfGOQHKeazR26EU')
# date_and_time = datetime.datetime.now().strftime('%H.%M.%S : %d-%m-%Y')
#
#
# async def job():
#     bot2.send_message(chat_id=2078991528, text='aaa')
#
#
# schedule.every(5).seconds.do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
