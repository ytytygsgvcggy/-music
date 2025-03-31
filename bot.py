from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

TOKEN = "7394131135:AAEBeZsGfQ1p21-YATTKiTfBDJ4QXZTzv3k"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a YouTube link to download the audio!")

def download_audio(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("Downloading audio...")

    opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = f"downloads/{info['title']}.mp3"

    update.message.reply_audio(audio=open(file_path, 'rb'))
    os.remove(file_path)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_audio))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    