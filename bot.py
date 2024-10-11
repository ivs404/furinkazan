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

# Укажите ваш логин и пароль Instagram
# Вместо этого вы можете использовать cookies
# Для использования cookies:
# L.load_session_from_file("your_username")  # Если у вас есть сохраненная сессия

# Или войдите в Instagram через cookies
cookies_file = 'cookies.json'  # Укажите путь к файлу с cookies
try:
    L.load_session_from_file("martin_06_10_24")  # Замените на ваш логин Instagram
except FileNotFoundError:
    logger.info("Файл с сессией не найден. Проверьте наличие cookies.")
    exit(1)

# Имя пользователя профиля, из которого хотите получать видео
profile_username = 'tvoretzz'  # Замените на желаемое имя пользователя

try:
    # Получаем профиль
    profile = instaloader.Profile.from_username(L.context, profile_username)
except instaloader.exceptions.ProfileNotExistsException:
    logger.error(f"Профиль {profile_username} не существует.")
    exit(1)

# Загрузка новых видео
def download_and_send_videos():
    for post in profile.get_posts():
        if post.typename == 'GraphVideo':
            logger.info(f"Загрузка видео: {post.shortcode}")
            # Загрузить видео
            video_url = post.video_url
            video_filename = f"{post.mediaid}.mp4"
            L.download_post(post, target=video_filename)

            # Отправить видео в Telegram
            with open(video_filename, 'rb') as video_file:
                bot.send_video(chat_id=CHANNEL_ID, video=video_file, caption=post.caption)

            # Удалить файл после отправки
            os.remove(video_filename)
            logger.info(f"Видео отправлено в Telegram: {post.shortcode}")

if __name__ == "__main__":
    download_and_send_videos()
