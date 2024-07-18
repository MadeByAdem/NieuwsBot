import latest_news
import telebot
import logging
import time
from ratelimit import limits, sleep_and_retry
from telebot import types
from cryptography.fernet import Fernet, InvalidToken
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
print(SECRET_KEY)

# Nieuws Feed bot
BOT_TOKEN=os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Global variable to keep track of users who want daily updates
wekservice_users_list = "./user_lists/wekservice_users.txt"
lunchservice_users_list = "./user_lists/lunchservice_users.txt"
avondservice_users_list = "./user_lists/avondservice_users.txt"


if not SECRET_KEY:
    logging.error("Secret key not set. Make sure to set the environment variable.")
    raise ValueError("Secret key not set. Make sure to set the environment variable.")

# Create logs directory if it doesn't exist
if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Set up logging configuration
logging.basicConfig(
    filename='./logs/news-telegram-bot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create user_lists directory if it doesn't exist
if not os.path.exists('./user_lists'):
    os.makedirs('./user_lists')

# Create avondservice_users.txt if it doesn't exist
if not os.path.exists(avondservice_users_list):
    with open(avondservice_users_list, 'w') as f:
        pass

# Create wekservice_users.txt if it doesn't exist
if not os.path.exists(wekservice_users_list):
    with open(wekservice_users_list, 'w') as f:
        pass

# Create lunchservice_users.txt if it doesn't exist
if not os.path.exists(lunchservice_users_list):
    with open(lunchservice_users_list, 'w') as f:
        pass

# Commands to copy into botFather
# help - Alle beschikbare commands in een lijst
# menu - Aan-/afmelden automatische berichten
# laatste_nieuws - Laatste nieuws (10 artikelen p/nieuwssite)
# f1_laatste_nieuws - Laatste Formule 1 nieuws
# binnenland_laatste_nieuws - Laatste binnenland nieuws
# buitenland_laatste_nieuws - Laatste buitenland nieuws
# politiek_laatste_nieuws - Laatste politiek nieuws
# sport_laatste_nieuws - Laatste sport nieuws
# tech_laatste_nieuws - Laatste tech nieuws
# wetenschap_laatste_nieuws - Laatste wetenschap nieuws
# opmerkelijk_laatste_nieuws - Laatste opmerkelijk nieuws
# nos_laatste_nieuws - Laatste NOS nieuws
# rtl_laatste_nieuws - Laatste RTL Nieuws
# ad_laatste_nieuws - Laatste AD nieuws
# volkskrant_laatste_nieuws - Laatste Volkskrant nieuws
# nrc_laatste_nieuws - Laatste NRC nieuws
# telegraaf_laatste_nieuws - Laatste Telegraaf nieuws
# nu_laatste_nieuws - Laatste Nu.nl nieuws


commands_telegram = """
<b>Help - Alle beschikbare commands in een lijst</b>
/help

<b>Wekservice - Aan- of afmelden voor de automatische berichten</b>
/menu

<b>Laatste nieuws (10 artikelen p/nieuwssite)</b>
/laatste_nieuws

<b>Formule1 - laatste nieuws</b>
/f1_laatste_nieuws

<b>Binnenland - laatste nieuws</b>
/binnenland_laatste_nieuws

<b>Buitenland - laatste nieuws</b>
/buitenland_laatste_nieuws

<b>Politiek - laatste nieuws</b>
/politiek_laatste_nieuws

<b>Sport - laatste nieuws</b>
/sport_laatste_nieuws

<b>Tech - laatste nieuws</b>
/tech_laatste_nieuws

<b>Wetenschap - laatste nieuws</b>
/wetenschap_laatste_nieuws

<b>Opmerkelijk - laatste nieuws</b>
/opmerkelijk_laatste_nieuws

<b>NOS - laatste nieuws</b>
/nos_laatste_nieuws

<b>RTL Nieuws - laatste nieuws</b>
/rtl_laatste_nieuws

<b>AD - laatste nieuws</b>
/ad_laatste_nieuws

<b>Volkskrant - laatste nieuws</b>
/volkskrant_laatste_nieuws

<b>NRC - laatste nieuws</b>
/nrc_laatste_nieuws

<b>Telegraaf - Laatste nieuws</b>
/telegraaf_laatste_nieuws

<b>Nu .nl - laatste nieuws</b>
/nu_laatste_nieuws
"""


# Encrypt the chat IDs before writing them to the file
def encrypt_chat_id(chat_id):
    logging.debug("Encrypt function started.")
    cipher_suite = Fernet(SECRET_KEY)
    encrypted_chat_id = cipher_suite.encrypt(str(chat_id).encode())
    logging.debug("Encrypt function ended.\n")
    return encrypted_chat_id


# Decrypt the chat IDs when reading from the file
def decrypt_chat_id(encrypted_chat_id):
    logging.debug("Decrypt function started.")
    try:
        cipher_suite = Fernet(SECRET_KEY)
        decrypted_id = cipher_suite.decrypt(encrypted_chat_id).decode()
        logging.debug("Decrypt function ended.\n")
        return decrypted_id
    except (InvalidToken, ValueError) as e:
        print(f"Error decrypting chat ID: {e}")
        logging.debug("Decrypt function ended.\n")
        return None


# Function to check if the user is already subscribed
def is_subscribed(chat_id, service):
    user_list = f"./user_lists/{service}_users.txt"
    logging.debug("Is_subscribed function started.")
    try:
        with open(f"{user_list}", "rb") as f:
            encrypted_chat_ids = f.read().splitlines()

        decrypted_chat_ids = [decrypt_chat_id(encrypted_id) for encrypted_id in encrypted_chat_ids if encrypted_id]

        logging.debug("Is_subscribed function ended.\n")
        return str(chat_id) in decrypted_chat_ids
    except FileNotFoundError:
        logging.info(FileNotFoundError)
        logging.debug("Is_subscribed function ended.\n")
        return False


# Limit the number of API requests to 30 per minute (adjust this as per Telegram API limits)
@sleep_and_retry
@limits(calls=30, period=60)
def send_message_with_rate_limit(bot, chat_id, text):
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    logging.debug(f"Handle_start function started.")
    global commands_telegram
    welcome_message = f"""Welkom! Deze bot voorziet in prikkelarme nieuwsfeeds.

Dit zijn de commands waar je gebruik van kan maken:

{commands_telegram}"""

    send_message_with_rate_limit(bot, message.chat.id, welcome_message)
    logging.info(f"Message: {message}")
    logging.debug(f"Handle_start function ended.\n")


# Function to handle the '/menu' command
@bot.message_handler(commands=['menu'])
def handle_menu(message):
    logging.debug(f"Handle_menu function started.")
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Check subscription
    is_user_subscribed_wekservice = is_subscribed(chat_id, "wekservice")
    is_user_subscribed_lunchservice = is_subscribed(chat_id, "lunchservice")
    is_user_subscribed_avondservice = is_subscribed(chat_id, "avondservice")

    # Change button text
    wekservice_text = 'Wekservice: staat aan' if is_user_subscribed_wekservice else 'Wekservice: staat uit'
    lunchservice_text = 'Lunchservice: staat aan' if is_user_subscribed_lunchservice else 'Lunchservice: staat uit'
    avondservice_text = 'Avondservice: staat aan' if is_user_subscribed_avondservice else 'Avondservice: staat uit'

    # Add buttons
    item1 = types.InlineKeyboardButton(wekservice_text, callback_data='Wekservice_toggle')
    item2 = types.InlineKeyboardButton(lunchservice_text, callback_data='Lunchservice_toggle')
    item3 = types.InlineKeyboardButton(avondservice_text, callback_data='Avondservice_toggle')
    markup.add(item1, item2, item3)

    # Option text
    option_selection_text = f"""<b>Selecteer een optie:</b>
- Wekservice: 06:30| alle platformen | laatste 10 artikelen
- Lunchservice: 12:00 | NOS & Nu .nl | laatste 10 artikelen
- Avondservice: 20:00 | alle platformen | laatste 10 artikelen
"""
    bot.send_message(chat_id, option_selection_text, reply_markup=markup)

    logging.debug(f"Handle_menu function ended.\n")


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    logging.debug(f"Handle_button_click function started.")
    if call.data == 'Wekservice_toggle':
        toggle_wekservice(call.message)
    elif call.data == 'Lunchservice_toggle':
        toggle_lunchservice(call.message)
    elif call.data == 'Avondservice_toggle':
        toggle_avondservice(call.message)

    logging.debug(f"Handle_button_click function ended.\n")


def toggle_wekservice(message):
    logging.debug(f"Toggle_wekservice function started.")
    chat_id = message.chat.id
    is_user_subscribed_wekservice = is_subscribed(chat_id, "wekservice")
    if is_user_subscribed_wekservice:
        send_message_with_rate_limit(bot, chat_id, "Je hebt je afgemeld voor de wekservice.")
        logging.info(f"User unsubscribed from wekservice")
    else:
        send_message_with_rate_limit(bot, chat_id,
                                     "Je hebt je aangemeld voor de wekservice. Iedere dag om 06:30 ontvang je het laatste nieuws.")
        logging.info(f"User subscribed to wekservice")

    # Toggle the subscription status (add or remove from users.txt)
    with open(wekservice_users_list, "rb") as f:
        encrypted_chat_ids = f.read().splitlines()

    decrypted_chat_ids = [decrypt_chat_id(encrypted_id) for encrypted_id in encrypted_chat_ids]

    with open(wekservice_users_list, "wb") as f:
        for decrypted_id in decrypted_chat_ids:
            if decrypted_id.strip() != str(chat_id):
                f.write(encrypt_chat_id(decrypted_id) + b'\n')

        if not is_user_subscribed_wekservice:
            f.write(encrypt_chat_id(str(chat_id)) + b'\n')
            logging.info(f"A user added to wekservice subscribe list")
        else:
            logging.info(f"A user removed from wekservice subscribe list")

    logging.debug(f"Toggle_wekservice function ended.\n")


def toggle_lunchservice(message):
    logging.debug(f"Toggle_lunchservice function started.")
    chat_id = message.chat.id
    is_user_subscribed_lunchservice = is_subscribed(chat_id, "lunchservice")
    if is_user_subscribed_lunchservice:
        send_message_with_rate_limit(bot, chat_id, "Je hebt je afgemeld voor de lunchservice.")
        logging.info(f"User unsubscribed from lunchservice")
    else:
        send_message_with_rate_limit(bot, chat_id,
                                     "Je hebt je aangemeld voor de lunchservice. Iedere dag om 12:00 ontvang je het laatste nieuws.")
        logging.info(f"User subscribed to lunchservice")

    # Toggle the subscription status (add or remove from users.txt)
    with open(lunchservice_users_list, "rb") as f:
        encrypted_chat_ids = f.read().splitlines()

    decrypted_chat_ids = [decrypt_chat_id(encrypted_id) for encrypted_id in encrypted_chat_ids]

    with open(lunchservice_users_list, "wb") as f:
        for decrypted_id in decrypted_chat_ids:
            if decrypted_id.strip() != str(chat_id):
                f.write(encrypt_chat_id(decrypted_id) + b'\n')

        if not is_user_subscribed_lunchservice:
            f.write(encrypt_chat_id(str(chat_id)) + b'\n')
            logging.info(f"A user added to lunchservice subscribe list")
        else:
            logging.info(f"A user removed from lunchservice subscribe list")

    logging.debug(f"Toggle_lunchservice function ended.\n")


def toggle_avondservice(message):
    logging.debug(f"Toggle_avondservice function started.")
    chat_id = message.chat.id
    is_user_subscribed_avondservice = is_subscribed(chat_id, "avondservice")
    if is_user_subscribed_avondservice:
        send_message_with_rate_limit(bot, chat_id, "Je hebt je afgemeld voor de avondservice.")
        logging.info(f"User unsubscribed from avondservice")
    else:
        send_message_with_rate_limit(bot, chat_id,
                                     "Je hebt je aangemeld voor de avondservice. Iedere dag om 20:00 ontvang je het laatste nieuws.")
        logging.info(f"User subscribed to avondservice")

    # Toggle the subscription status (add or remove from users.txt)
    with open(avondservice_users_list, "rb") as f:
        encrypted_chat_ids = f.read().splitlines()

    decrypted_chat_ids = [decrypt_chat_id(encrypted_id) for encrypted_id in encrypted_chat_ids]

    with open(avondservice_users_list, "wb") as f:
        for decrypted_id in decrypted_chat_ids:
            if decrypted_id.strip() != str(chat_id):
                f.write(encrypt_chat_id(decrypted_id) + b'\n')

        if not is_user_subscribed_avondservice:
            f.write(encrypt_chat_id(str(chat_id)) + b'\n')
            logging.info(f"A user added to avondservice subscribe list")
        else:
            logging.info(f"A user removed from avondservice subscribe list")

    logging.debug(f"Toggle_avondservice function ended.\n")


@bot.message_handler(commands=['laatste_nieuws'])
def handle_latest_news(message):
    logging.debug(f"Handle_latest_news started.")

    num_of_articles = 10

    news_message = f"<b>Hier is het laatste nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_message = latest_news.nos_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_message)

    rtl_message = latest_news.rtl_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, rtl_message)

    ad_message = latest_news.ad_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_message)

    volkskrant_message = latest_news.volkskrant_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, volkskrant_message)

    nrc_message = latest_news.nrc_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_message)

    telegraaf_message = latest_news.telegraaf_voorpagina_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, telegraaf_message)

    nu_message = latest_news.nu_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nu_message)

    logging.debug(f"Handle_latest_news function ended.\n")


@bot.message_handler(commands=['politiek_laatste_nieuws'])
def handle_politiek_latest_news(message):
    logging.debug(f"Handle_politiek_latest_news started.")

    num_of_articles = 10

    news_message = f"<b>Hier is het laatste politieke nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_politiek_message = latest_news.nos_politiek_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_politiek_message)

    ad_politiek_message = latest_news.ad_politiek_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_politiek_message)

    nrc_politiek_message = latest_news.nrc_politiek_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_politiek_message)

    logging.debug(f"Handle_politiek_latest_news ended.\n")


@bot.message_handler(commands=['binnenland_laatste_nieuws'])
def handle_binnenland_latest_news(message):
    logging.debug(f"Handle_binnenland_latest_news started.")

    num_of_articles = 10

    news_message = f"<b>Hier is het laatste binnenlands nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_binnenland_message = latest_news.nos_nieuws_binnenland_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_binnenland_message)

    ad_binnenland_message = latest_news.ad_binnenland_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_binnenland_message)

    nrc_binnenland_message = latest_news.nrc_binnenland_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_binnenland_message)

    logging.debug(f"Handle_binnenland_latest_news ended.\n")


@bot.message_handler(commands=['buitenland_laatste_nieuws'])
def handle_buitenland_latest_news(message):
    logging.debug(f"Handle_buitenland_latest_news started.")

    num_of_articles = 10

    news_message = f"<b>Hier is het laatste buitenlands nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_buitenland_message = latest_news.nos_nieuws_buitenland_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_buitenland_message)

    ad_buitenland_message = latest_news.ad_buitenland_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_buitenland_message)

    nrc_buitenland_message = latest_news.nrc_buitenland_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_buitenland_message)

    logging.debug(f"Handle_buitenland_latest_news ended.\n")


@bot.message_handler(commands=['sport_laatste_nieuws'])
def handle_sport_latest_news(message):
    logging.debug(f"Handle_sport_latest_news started.")

    num_of_articles = 10

    news_message = f"<b>Hier is het laatste sport nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_sport_message = latest_news.nos_sport_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_sport_message)

    ad_sport_message = latest_news.ad_sport_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_sport_message)

    volkskrant_sport_message = latest_news.volkskrant_sport_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, volkskrant_sport_message)

    nrc_sport_message = latest_news.nrc_sport_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_sport_message)

    telegraaf_sport_message = latest_news.telegraaf_sport_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, telegraaf_sport_message)

    nu_sport_message = latest_news.nu_sport_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nu_sport_message)

    logging.debug(f"Handle_sport_latest_news ended.\n")


@bot.message_handler(commands=['f1_laatste_nieuws'])
def handle_f1_latest_news(message):
    logging.debug(f"Handle_f1_latest_news started.")

    num_of_articles = 7

    news_message = f"<b>Hier is het laatste Formule 1 nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    formule1_message = latest_news.formule1nl_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, formule1_message)

    nos_formule1_message = latest_news.nos_sport_formule1_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_formule1_message)

    ad_formule1_message = latest_news.ad_formule1_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_formule1_message)

    logging.debug(f"Handle_f1_latest_news ended.\n")


@bot.message_handler(commands=['tech_laatste_nieuws'])
def handle_tech_latest_news(message):
    logging.debug(f"Handle_tech_latest_news started.")

    num_of_articles = 5

    news_message = f"<b>Hier is het laatste tech nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_tech_message = latest_news.nos_nieuws_tech_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_tech_message)

    rtl_tech_message = latest_news.rtl_tech_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, rtl_tech_message)

    nu_tech_message = latest_news.nu_tech_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nu_tech_message)

    bright_tech_message = latest_news.bright_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, bright_tech_message)

    logging.debug(f"Handle_tech_latest_news ended.\n")


@bot.message_handler(commands=['wetenschap_laatste_nieuws'])
def handle_wetenschap_latest_news(message):
    logging.debug(f"Handle_wetenschap_latest_news started.")

    num_of_articles = 5

    news_message = f"<b>Hier is het laatste wetenschap nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    ad_wetenschap_message = latest_news.ad_wetenschap_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_wetenschap_message)

    volkskrant_wetenschap_message = latest_news.volkskrant_wetenschap_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, volkskrant_wetenschap_message)

    nrc_wetenschap_message = latest_news.nrc_wetenschap_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_wetenschap_message)

    nu_wetenschap_message = latest_news.nu_wetenschap_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nu_wetenschap_message)

    logging.debug(f"Handle_wetenschap_latest_news ended.\n")


@bot.message_handler(commands=['opmerkelijk_laatste_nieuws'])
def handle_opmerkelijk_latest_news(message):
    logging.debug(f"Handle_opmerkelijk_latest_news started.")

    num_of_articles = 5

    news_message = f"<b>Hier is het laatste opmerkelijk nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_opmerkelijk_message = latest_news.nos_nieuws_opmerkelijk_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_opmerkelijk_message)

    ad_opmerkelijk_message = latest_news.ad_bizar_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_opmerkelijk_message)

    nu_opmerkelijk_message = latest_news.nu_opmerkelijk_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nu_opmerkelijk_message)

    logging.debug(f"Handle_opmerkelijk_latest_news ended.\n")


@bot.message_handler(commands=['nos_laatste_nieuws'])
def handle_nos_latest_news(message):
    logging.debug(f"Handle_nos_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste NOS nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nos_message = latest_news.nos_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nos_message)

    logging.debug(f"Handle_nos_latest_news ended.\n")


@bot.message_handler(commands=['rtl_laatste_nieuws'])
def handle_rtl_latest_news(message):
    logging.debug(f"Handle_rtl_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste RTL nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    rtl_message = latest_news.rtl_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, rtl_message)

    logging.debug(f"Handle_rtl_latest_news ended.\n")


@bot.message_handler(commands=['ad_laatste_nieuws'])
def handle_ad_latest_news(message):
    logging.debug(f"Handle_ad_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste AD nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    ad_message = latest_news.ad_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, ad_message)

    logging.debug(f"Handle_ad_latest_news ended.\n")


@bot.message_handler(commands=['volkskrant_laatste_nieuws'])
def handle_volkskrant_latest_news(message):
    logging.debug(f"Handle_volkskrant_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste Volkskrant nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    volkskrant_message = latest_news.volkskrant_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, volkskrant_message)

    logging.debug(f"Handle_volkskrant_latest_news ended.\n")


@bot.message_handler(commands=['nrc_laatste_nieuws'])
def handle_nrc_latest_news(message):
    logging.debug(f"Handle_nrc_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste NRC nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nrc_message = latest_news.nrc_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nrc_message)

    logging.debug(f"Handle_nrc_latest_news ended.\n")


@bot.message_handler(commands=['telegraaf_laatste_nieuws'])
def handle_telegraaf_latest_news(message):
    logging.debug(f"Handle_telegraaf_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste Telegraaf nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    telegraaf_message = latest_news.telegraaf_voorpagina_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, telegraaf_message)

    logging.debug(f"Handle_telegraaf_latest_news ended.\n")


@bot.message_handler(commands=['nu_laatste_nieuws'])
def handle_nu_latest_news(message):
    logging.debug(f"Handle_nu_latest_news started.")

    num_of_articles = 15

    news_message = f"<b>Hier is het laatste NU.nl nieuws:</b>"
    send_message_with_rate_limit(bot, message.chat.id, news_message)

    nu_message = latest_news.nu_algemeen_recent_articles(num_of_articles)
    send_message_with_rate_limit(bot, message.chat.id, nu_message)

    logging.debug(f"Handle_nu_latest_news ended.\n")


@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    logging.debug(f"Handle_all_other_messages function started.")
    # Code to execute for all other messages (archive bot function)
    
    if message.text and message.text.strip():
        try:
            output = get_archive_url(message.text)
            if output:
                bot.reply_to(message, output)
            else:
                bot.reply_to(message, "Send me an url, and I'll try to get the archive url for you.")
        except Exception as e:
            print(f"Error fetching the URL: {e}")
            bot.reply_to(message, "An error occurred while fetching the URL.")
        

    logging.debug(f"Handle_all_other_messages function ended.")

# If user sends a url, get the latest archive.today url for that url
def get_archive_url(url):
    # Extract the URL from the message text using regular expressions
    match = re.search(r"(?P<url>https?://[^\s]+)", url)
    if match:
        archive_url = 'https://archive.today/newest/'
        input_modified = f'{archive_url}{match.group("url")}'
        return input_modified
    else:
        return None

print("Bot running...")
logging.info("Bot running...")
bot.polling()
