import instaloader
import telegram
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Настройки Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получите токен через @BotFather
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ID вашего Telegram-канала

bot = telegram.Bot(token=BOT_TOKEN)

# Настройка Instaloader
L = instaloader.Instaloader()

# Ваши учетные данные Instagram
instagram_username = 'martin_06_10_24'  # Замените на ваш логин
instagram_password = 'g8bRncEvHdxfMKY'  # Замените на ваш пароль

# Вход в Instagram
L.login(instagram_username, instagram_password)

# Укажите Instagram аккаунт, из которого нужно загружать видео
username = "tvoretzz"

# Получаем профиль
try:
    profile = instaloader.Profile.from_username(L.context, username)
except instaloader.exceptions.ProfileNotExistsException:
    logger.error(f'Профиль "{username}" не существует.')
    exit()

# Загрузка новых видео
def download_and_send_videos():
    for post in profile.get_posts():
        if post.typename == 'GraphVideo':
            # Загрузить видео
            video_url = post.video_url
            video_filename = f"{post.mediaid}.mp4"
            L.download_post(post, target=video_filename)

            # Отправить видео в Telegram
            with open(video_filename, 'rb') as video_file:
                bot.send_video(chat_id=CHANNEL_ID, video=video_file, caption=post.caption)

            # Удалить файл после отправки
            os.remove(video_filename)

if __name__ == "__main__":
    download_and_send_videos()
