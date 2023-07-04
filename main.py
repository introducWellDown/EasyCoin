import telebot
import requests
import threading
import time
import re
from telebot import types
from bs4 import BeautifulSoup
from private import token
from bd import isExistsID
from bd import outputValues
from bd import updateValue
from bd import changeNotificationStatus
from bd import createBD
from bd import outputSingleValues
from bd import chekNotificationStatus

# Для удобства разрабтки, это будет раздел со всомогательными функциями.

createBD()

# Автоперезапуск при падении
def startBot():     
    while True:
        try:
            print("start pooling ;)") 
            bot.polling()
            print("stop pooling !")
        except Exception as e:
            print("Произошла ошибка:", e)    
            time.sleep(3) 
    

valuetList = ["Eth","Bitcoin"]  

about = "Со мной, ты можешь отслеживать актуальные цены на криптовалюты!\n\n" \
        "Также, ты можешь установить цену на валюту и я сообщу тебе, когда стоимость станет равной твоей!\n\n" \
        "Вот краткое описание моих функций:\n" \
        "1.Цены валют - В этом разделе ты можешь просмотреть актуальные цены криптовалют.\n" \
        "Информация берется с ресурса <www.coingecko.com>\n" \
        "2.Установленные цены - здесь ты можешь посмотреть, какую стоимость валюты ты уже отслеживаешь.\n" \
        "3.Изменить установленные цены - здесь ты можешь изменить уже установленные цены. \n" \
        "4.Включить / Выключить уведомления - по умолчанию, эта функция выключена, если хочешь получать уведомления о соответствии цен, то здесь это можно сделать." 
    
def showValuetlist():
    result = ""
    for valuet in valuetList:
        result += valuet + "\n" 
    return result
        
def show_price(coin):
    url = 'https://www.coingecko.com/ru'

    response = requests.get(url, headers={'User-Agent':
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/104.0.5112.79 "
                            "Safari/537.36"}, timeout=15).text

    soup = BeautifulSoup(response, 'html.parser')
    if coin == 'Bitcoin':
        priceBtc = soup.find('span', {'class': 'no-wrap', 'data-coin-symbol': 'btc'}).text
        return (str(priceBtc).replace("$","") + " $") 
    elif coin == 'Eth':
        priceEth = soup.find('span', {'class': 'no-wrap', 'data-coin-symbol': 'eth'}).text
        return (str(priceEth).replace("$","") + " $")       


 
# Функция для периодической проверки
def controlNotification(message):
    while True:
        if chekNotificationStatus(message.chat.id):
            time.sleep(10)
            checkPrice(message.chat.id, "Eth")
            checkPrice(message.chat.id, "Bitcoin")
        else:
            break

def run_controlNotification(message, status):
    thread = threading.Thread(target=controlNotification, args=(message,))
    thread.daemon = True  # Устанавливаем поток в режим демона
    if status == True:
        thread.start()  # Запускаем поток только если status равен True
        thread.join()   # Дожидаемся завершения потока
        
 # Функция для проверки соответствия цены валюты заданному диапазону

def checkPrice(userId, coin):
    
    user_price = outputSingleValues((userId), coin)
    current_price = float(show_price(coin).replace("$", "").replace(" ","").replace(",","."))
    
    if (user_price - 20 <= current_price <= user_price + 20) :
        message = f"{coin} находится в диапазоне +-20 $ от установленной вами цены!"
        bot.send_message(userId, message)
 
        
# На этапе тестов этого бота на своих знакомых,я заметил ,что многие ошибаются с вводом        
# новой стоимости для отслеживания. Вводят все,что угодно,но не то,что нужно.
# Для решения этой проблемы я решил использовать регулярное выражение,
# для корректировки пользовательского ввода

def extract_numbers(user_input):
    numbers = re.findall(r'\d+',user_input)
    if numbers:
        return ''.join(numbers)
    else:
        return 0

# Создаем переменную с токеном бота


bot = telebot.TeleBot(token)

 

main = types.KeyboardButton(text = 'Главное меню')

@bot.message_handler(commands=['start'])
def start(message):
    
    isExistsID(message.chat.id,message.from_user.first_name)
    # Создаем клавиатуру для использования функционала бота
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width = 1)
    
    priceBtn = types.KeyboardButton(text='Цены валют')
    myPriceBtn = types.KeyboardButton(text='Просмотреть установленные цены')
    changePriceBtn = types.KeyboardButton(text='Изменить установленные цены')
    pushBtn =  types.KeyboardButton(text='Включить / Выключить уведомления')
    aboutBtn =  types.KeyboardButton(text='Описание функций')
    
    kb.add(priceBtn,myPriceBtn,changePriceBtn,pushBtn,aboutBtn)
    
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}!',reply_markup = kb)

    
    
    
# Добавляем обработчики для кнопок
@bot.message_handler(func = lambda message: message.text == 'Цены валют')
def handle_price(message):
    # Cоздаем клавиатуру для выбора нужной валюты
    valuesKb = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width = 1)
    
    ethBtn = types.KeyboardButton(text='Eth')
    btcBtn = types.KeyboardButton(text='Bitcoin')
    
    
    valuesKb.add(ethBtn,btcBtn,main)
    
    bot.send_message(message.chat.id,f'Выбери валюту из списка:\n{showValuetlist()} ',reply_markup = valuesKb)

@bot.message_handler(func = lambda message: message.text == 'Eth')
def sendPrice(message):
    bot.send_message(message.chat.id,show_price(message.text))

@bot.message_handler(func = lambda message: message.text == 'Bitcoin')
def sendPrice(message):
    bot.send_message(message.chat.id,show_price(message.text))   

@bot.message_handler(func=lambda message: message.text == 'Просмотреть установленные цены')
def handle_my_price(message):
    bot.send_message(message.chat.id,outputValues(message.chat.id))

@bot.message_handler(func=lambda message: message.text == 'Изменить установленные цены')
def handle_change_price(message):
    
    valuesKb = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width = 1)
    
    ethBtn = types.KeyboardButton(text='Изменить цену ETH')
    btcBtn = types.KeyboardButton(text='Изменить цену Bitcoin')
    
    
    valuesKb.add(ethBtn,btcBtn,main)
    bot.send_message(message.chat.id,f'Выбери валюту для изменения:\n{showValuetlist()} ',reply_markup = valuesKb)
    
@bot.message_handler(func=lambda message: message.text == 'Изменить цену ETH')
def handle_eth_price(message):
    bot.send_message(message.chat.id, 'Введите стоимость, по которой хотите отслеживать:')
    bot.register_next_step_handler(message, handle_eth_price_input)

def handle_eth_price_input(message):
    if message.text.isdigit():
        user_input = int(message.text)
        updateValue(message.chat.id, "Eth", user_input)
        bot.send_message(message.chat.id, "Стоимость ETH успешно изменена.")
    else:
        user_input = extract_numbers(message.text)
        updateValue(message.chat.id, "Eth", user_input)
        bot.send_message(message.chat.id, "Стоимость ETH успешно изменена.")
   
@bot.message_handler(func=lambda message: message.text == 'Изменить цену Bitcoin')
def handle_Bitcoin_price(message):
    bot.send_message(message.chat.id, 'Введите стоимость, по которой хотите отслеживать:')
    bot.register_next_step_handler(message, handle_Bitcoin_price_input)

def handle_Bitcoin_price_input(message):
    if message.text.isdigit():
        user_input = int(message.text)
        updateValue(message.chat.id, "Bitcoin", user_input)
        bot.send_message(message.chat.id, "Стоимость Bitcoin успешно изменена.")
    else:
        user_input = extract_numbers(message.text)
        updateValue(message.chat.id, "Bitcoin", user_input)
        bot.send_message(message.chat.id, "Стоимость Bitcoin успешно изменена.")

@bot.message_handler(func=lambda message: message.text == 'Включить / Выключить уведомления')
def handle_push(message):
    changeNotificationStatus(message.chat.id)
    status = chekNotificationStatus(message.chat.id)
    if status == False:
        bot.send_message(message.chat.id, "Уведомления выключены!")
        run_controlNotification(message,status) 
    if status == True:
        bot.send_message(message.chat.id, "Уведомления включены!")
        run_controlNotification(message,status)

@bot.message_handler(func = lambda message: message.text == 'Главное меню')
def showMenu(message):    
    # Создаем клавиатуру для использования функционала бота
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width = 1)
    
    priceBtn = types.KeyboardButton(text='Цены валют')
    myPriceBtn = types.KeyboardButton(text='Просмотреть установленные цены')
    changePriceBtn = types.KeyboardButton(text='Изменить установленные цены')
    pushBtn =  types.KeyboardButton(text='Включить / Выключить уведомления')
    aboutBtn =  types.KeyboardButton(text='Описание функций')
    
    kb.add(priceBtn,myPriceBtn,changePriceBtn,pushBtn,aboutBtn)
    
    bot.send_message(message.chat.id,text="Выберите действие из списка", reply_markup=kb)

# Добавляем вывод Описания функционала
@bot.message_handler(func = lambda message: message.text == 'Описание функций')
def showFunctionDescription(message):
    kbMain = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width = 1)
    kbMain.add(main)
    
    bot.send_message(message.chat.id,text=about, reply_markup=kbMain)



startBot()
