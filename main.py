from telebot import types

from settings import ADMIN_ID, bot, ALL_BUTTONS
from database import *

status_activity = {}
temp_list = []


@bot.message_handler(commands=['start'])
def checkUser(message):

    create_new_table()
    check_on_availability(message.chat.id, message.from_user.first_name)

    if IsAdmin(message.chat.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        # Используем итератор с шагом 2, чтобы добавлять кнопки парами в ряды
        buttons = [types.KeyboardButton(btn) for btn in ALL_BUTTONS]

        # Добавляем кнопки парами
        for i in range(0, len(buttons), 2):
            markup.row(*buttons[i:i + 2])

        bot.send_message(message.chat.id, "Выберите кнопку", reply_markup=markup)

    else:
        ShowAllLinks(message.chat.id)


def ShowAllLinksForAdmin(user_id):
    markup = types.InlineKeyboardMarkup()
    links = show_all_link_for_admin()

    for element in links:
        number, name, link = element
        markup.add(types.InlineKeyboardButton(f"{number} | {name}", url=link))

    bot.send_message(user_id, "Список чатов:", reply_markup=markup)


def ShowAllLinks(user_id):
    markup = types.InlineKeyboardMarkup()
    links = show_all_link()

    for element in links:
        name, link = element
        markup.add(types.InlineKeyboardButton(name, url=link))

    bot.send_message(user_id, "Добрый день! Список чатов:", reply_markup=markup)


def IsAdmin(user_id):
    return str(user_id) in ADMIN_ID



@bot.message_handler(func=lambda message: True)
def messageMain(message):

    user_id = message.chat.id
    global temp_list

    if message.text == ALL_BUTTONS[0]:

        ShowAllLinksForAdmin(user_id)

    elif message.text == ALL_BUTTONS[1]:
        temp_list = []
        bot.send_message(user_id, "Введите название магазина: ")
        status_activity[user_id] = 'input_name'
    elif message.text == ALL_BUTTONS[2]:
        bot.send_message(user_id, "Введите номер магазина, который хотите удалить")
        status_activity[user_id] = 'input_delete_number'

    elif message.text == ALL_BUTTONS[3]:
        bot.send_message(user_id, "Введите текст рассылки: ")
        status_activity[user_id] = 'input_text'

    elif status_activity.get(user_id) == 'input_delete_number':
        try:
            delete_row_by_id(message.text)
            bot.send_message(user_id, 'Готово! Магазин удален.')
        except Exception as e:
            bot.send_message(user_id, f'Ошибка. Возможно введен некоректный номер. Код ошибка: {e}')

    elif status_activity.get(user_id) == 'input_text':
        bot.send_message(user_id, f'Ваш текст: \n{message.text}')

        btn1 = 'Да'
        btn2 = 'Нет'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(btn1, btn2)

        bot.send_message(user_id, 'Подтвердите отправку', reply_markup = markup)
        status_activity[user_id] = message.text

    elif message.text == 'Да' and IsAdmin(user_id):
        send_broadcast_message(status_activity.get(user_id))
        checkUser(message)

    elif message.text == 'Нет' and IsAdmin(user_id):
        checkUser(message)

    elif status_activity.get(user_id) == 'input_name':
        temp_list.append(message.text)
        bot.send_message(user_id, "Введите ссылку на магазин: ")
        status_activity[user_id] = 'input_link'

    elif status_activity.get(user_id) == 'input_link':
        temp_list.append(message.text)
        add_link(str(temp_list[0]), str(temp_list[1]))

        bot.send_message(user_id, 'Информация успешно сохранена')
        status_activity[user_id] = None
        temp_list = []


def send_broadcast_message(message_text):
    user_ids = get_all_user_ids()  # Получаем всех пользователей
    count_complete = 0
    count_mistake = 0
    for user_id in user_ids:
        try:
            bot.send_message(user_id, message_text)  # Отправляем сообщение
            count_complete += 1
        except Exception as e:
            count_mistake += 1
    for admin in ADMIN_ID:
        bot.send_message(admin, f"Рассылка завершена. Успешно отрпавленных сообщений: {count_complete}. Не удалось отправить сообщения: {count_mistake}")




bot.polling(none_stop=True)
