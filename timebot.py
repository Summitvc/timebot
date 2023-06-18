from lxml import html
import requests 
import time
import telebot

TOKEN = ''
bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start']) 
def send_welcome(message):
    bot.reply_to(message, 'Use /choose')   


@bot.message_handler(commands=['choose']) 
def choose_option(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    keyboard.row(
        telebot.types.InlineKeyboardButton('Seconds to next year', callback_data='get-SEC'),
        telebot.types.InlineKeyboardButton('Minutes to next year', callback_data='get-MIN')
    )
    
    keyboard.row(
        telebot.types.InlineKeyboardButton('Hours to next year', callback_data='get-HOURS'),
        telebot.types.InlineKeyboardButton('Days to next year', callback_data='get-DAYS')
    )
    keyboard.row(
    	telebot.types.InlineKeyboardButton('Everything together', callback_data='get-ALL')
    )

    bot.send_message(  
        message.chat.id,   
        'Choose any option you want:',  
        reply_markup=keyboard  
    )

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'get-SEC':

        page = requests.get('https://www.timeanddate.com/counters/newyear.html')
        tree = html.fromstring(page.content)
        countdown_sec = tree.xpath('//*[@id="el_s2"]/text()')
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=countdown_sec[0]+" seconds to the next year.")
    if call.data == 'get-MIN':

        page = requests.get('https://www.timeanddate.com/counters/newyear.html')
        tree = html.fromstring(page.content)
        countdown_min = tree.xpath('//*[@id="el_m2"]/text()') 

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=countdown_min[0]+" minutes to the next year.")
    if call.data == 'get-HOURS':

        page = requests.get('https://www.timeanddate.com/counters/newyear.html')
        tree = html.fromstring(page.content)
        countdown_hours = tree.xpath('//*[@id="el_h2"]/text()')    

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=countdown_hours[0]+" hours to the next year.")
    if call.data == 'get-DAYS':

        page = requests.get('https://www.timeanddate.com/counters/newyear.html')
        tree = html.fromstring(page.content)
        countdown_days = tree.xpath('//*[@id="el_d2"]/text()')  

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=countdown_days[0]+" days to next year.")
    if call.data == 'get-ALL':
        timer = 10

        while timer > 0:
            page = requests.get('https://www.timeanddate.com/counters/newyear.html')
            tree = html.fromstring(page.content)

            countdown_sec = tree.xpath('//*[@id="el_s2"]/text()')
            countdown_min = tree.xpath('//*[@id="el_m2"]/text()') 
            countdown_hours = tree.xpath('//*[@id="el_h2"]/text()')    
            countdown_days = tree.xpath('//*[@id="el_d2"]/text()') 

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=str(countdown_days[0])+" days: "+str(countdown_hours[0])+" hours: "+str(countdown_min[0])+" minutes: "+str(countdown_sec[0])+" seconds")
            timer-=1
            time.sleep(1)



while True:
    try:        
        bot.polling()
    except Exception:
        time.sleep(15)

