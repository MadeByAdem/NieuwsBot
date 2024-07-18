import logging
import telebot
import schedule
import time
import latest_news
from cryptography.fernet import Fernet
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("Secret key not set. Make sure to set the environment variable.")

# Create logs directory if it doesn't exist
if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Set up logging configuration
logging.basicConfig(
    filename='./logs/news-schedule-telegram-bot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Nieuws Feed bot
BOT_TOKEN=os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


def decrypt_chat_id(encrypted_chat_id):
    logging.debug("Decrypt function started.")
    cipher_suite = Fernet(SECRET_KEY)
    decrypted_chat_id = cipher_suite.decrypt(encrypted_chat_id).decode()
    logging.debug("Decrypt function ended.\n")
    return decrypted_chat_id


def send_daily_news(service):
    logging.debug(f"Send_daily_news function started.")
    with open(f"./user_lists/{service}_users.txt", "rb") as f:
        encrypted_chat_ids = f.read().splitlines()

    for encrypted_id in encrypted_chat_ids:
        chat_id = decrypt_chat_id(encrypted_id).strip()
        if service == "wekservice":
            send_wekservice(chat_id)
        elif service == "lunchservice":
            send_lunchservice(chat_id)
        elif service == "avondservice":
            send_avondservice(chat_id)

    logging.info("Daily messages sent.")
    logging.debug(f"Send_daily_news function ended.\n")


def send_wekservice(chat_id):
    logging.debug("Send_wekservice function started.")
    num_of_articles = 10

    news_message = f"""<b>🌄 Goedemorgen!

Hier is het laatste nieuws van deze ochtend.

Fijne dag vandaag! 💪🏻</b>"""

    bot.send_message(chat_id, news_message)

    nos_message = latest_news.nos_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nos_message)

    rtl_message = latest_news.rtl_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, rtl_message)

    ad_message = latest_news.ad_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, ad_message)

    volkskrant_message = latest_news.volkskrant_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, volkskrant_message)

    nrc_message = latest_news.nrc_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nrc_message)

    telegraaf_message = latest_news.telegraaf_voorpagina_recent_articles(num_of_articles)
    bot.send_message(chat_id, telegraaf_message)

    nu_message = latest_news.nu_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nu_message)

    logging.debug("Send_wekservice function ended.\n")


def send_lunchservice(chat_id):
    logging.debug("Send_lunchservice function started.")
    num_of_articles = 10

    news_message = f"""<b>🥪 Goedemiddag!

Hier is het laatste nieuws.

Eet smakelijk!😋</b>"""

    bot.send_message(chat_id, news_message)

    nos_message = latest_news.nos_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nos_message)

    nu_message = latest_news.nu_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nu_message)

    logging.debug("Send_lunchservice function ended.\n")


def send_avondservice(chat_id):
    logging.debug("Send_avondservice function started.")
    num_of_articles = 10

    news_message = f"""<b>🌜 Goedenavond!

Hier is het laatste nieuws van vandaag.

Fijne avond! 🌛</b>"""

    bot.send_message(chat_id, news_message)

    nos_message = latest_news.nos_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nos_message)

    rtl_message = latest_news.rtl_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, rtl_message)

    ad_message = latest_news.ad_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, ad_message)

    volkskrant_message = latest_news.volkskrant_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, volkskrant_message)

    nrc_message = latest_news.nrc_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nrc_message)

    telegraaf_message = latest_news.telegraaf_voorpagina_recent_articles(num_of_articles)
    bot.send_message(chat_id, telegraaf_message)

    nu_message = latest_news.nu_algemeen_recent_articles(num_of_articles)
    bot.send_message(chat_id, nu_message)

    logging.debug("Send_avondservice function ended.\n")


# Schedule the task without calling the function directly
schedule.every().day.at("06:30").do(lambda: send_daily_news("wekservice"))
print("Wekservice scheduled for 06:30!")
logging.debug("Wekservice scheduled for 06:30!")

schedule.every().day.at("12:00").do(lambda: send_daily_news("lunchservice"))
print("Lunchservice scheduled for 12:00!")
logging.debug("Lunchservice scheduled for 12:00!")


schedule.every().day.at("20:00").do(lambda: send_daily_news("avondservice"))
print("Avondservice scheduled for 20:00!")
logging.debug("Avondservice scheduled for 20:00!")

while True:
    schedule.run_pending()
    time.sleep(1)
