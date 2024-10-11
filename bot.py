import instaloader
import telegram
import logging
import os
from time import sleep

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Настройки Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получите токен через @BotFather
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ID вашего Telegram-канала
bot = telegram.Bot(token=BOT_TOKEN)

# Настройка Instaloader
L = instaloader.Instaloader()

# Укажите Instagram аккаунт для отслеживания
ACCOUNT_NAME = 'tvoretzz'

# Хранение последнего обработанного поста
last_post_id_file = 'last_post_id.txt'

def get_last_post_id():
    try:
        with open(last_post_id_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_last_post_id(post_id):
    with open(last_post_id_file, 'w') as file:
        file.write(post_id)

def send_video_to_telegram(video_url):
    bot.send_message(chat_id=CHANNEL_ID, text=video_url)

# Главный цикл для проверки новых постов
while True:
    profile = instaloader.Profile.from_username(L.context, ACCOUNT_NAME)
    latest_post = next(profile.get_posts())

    # Получение ID последнего поста
    last_post_id = get_last_post_id()

    # Если это новый пост, отправляем его в Telegram
    if last_post_id != latest_post.shortcode:
        video_url = f"https://www.instagram.com/p/{latest_post.shortcode}/"
        send_video_to_telegram(video_url)
        save_last_post_id(latest_post.shortcode)
        logger.info(f"New video sent to Telegram: {video_url}")

    sleep(300)  # Пауза в 5 минут перед следующей проверкой
