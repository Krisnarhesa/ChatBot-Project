import datetime
import os
import time
import requests
import telebot
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.getenv('TOKEN_BOT')

bot = telebot.TeleBot(token)

url = os.getenv('URL_API')

# Fungsi untuk mengirim pesan pengguna ke URL dan mengambil responsnya
def get_response_from_url(message_text):
    try:
        response = requests.get(url.replace('inputuser', message_text))
        response_json = response.json()
        response_text = response_json.get('response', 'Maaf, tidak ada respons').strip()
        return response_text
    except Exception as e:
        print("Error:", e)
        return "Maaf, ada masalah saat memproses permintaan Anda."

# Fungsi untuk merekam log pengguna
def log_user_message(message):
    with open("user_logs.txt", "a", encoding="utf-8") as log_file:
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = message.from_user.username if message.from_user.username else "Unknown"
        log_file.write(f"{log_time} - User ID: {message.from_user.id}, Username: {username}, Message: {message.text}\n")

# Fungsi untuk merekam log respon bot
def log_bot_response(message, response):
    with open("AI_bot_responses.txt", "a", encoding="utf-8") as log_file:
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = message.from_user.username if message.from_user.username else "Unknown"
        log_file.write(f"{log_time} - User ID: {message.from_user.id}, Username: {username}, Response: {response}\n")

# Fungsi untuk merekam log feedback
def log_feedback(message):
    with open("feedbacks.txt", "a", encoding="utf-8") as log_file:
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = message.from_user.username if message.from_user.username else "Unknown"
        feedback_text = message.text.replace('/feedback', '').strip()
        log_file.write(f"{log_time} - User ID: {message.from_user.id}, Username: {username}, Feedback: {feedback_text}\n")

# Fungsi menjawab dan mengambil pesan pengguna dan memberikan respons dari URL
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Jika pesan adalah perintah, tangani sesuai dengan jenis perintahnya
    if message.text.startswith('/'):
        if message.text.startswith('/start'):
            send_welcome(message)
        elif message.text.startswith('/help'):
            send_help(message)
        elif message.text.startswith('/assignment'):
            send_assignment_request(message)
        elif message.text.startswith('/feedback'):
            send_feedback(message)
    else:
        # Mengambil respons dari URL yang diberikan dengan pesan pengguna
        response_from_url = get_response_from_url(message.text)
        bot.reply_to(message, response_from_url)
        log_bot_response(message, response_from_url)
        log_user_message(message)

# Fungsi untuk menyambut pengguna ketika memulai atau meminta bantuan
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Tecartbot, I am a bot that can help you with your assignment bro. Send me the assignment and I will finish it for you. use / or /help to see the detail available commands or just chat anything and AI will respond to you :)")
    log_user_message(message)

# Fungsi untuk menampilkan panduan penggunaan bot
def send_help(message):
    commands_list = "/start - Start the bot & welcome message.\n/assignment - Send me the Tubes/Modul Praktikum you want me to finish for you.\n/help - Display this help message.\n/feedback  'Your Feedback'  - Send feedback to the developer :)"
    bot.reply_to(message, "Available commands:\n" + commands_list)
    log_user_message(message)

# Fungsi untuk meminta pengguna untuk memberikan tugas
def send_assignment_request(message):
    bot.reply_to(message, "Send me the assignment you want me to finish for you.")
    log_user_message(message)

# Fungsi untuk mengirimkan feedback kepada pengembang bot
def send_feedback(message):
    feedback_text = message.text.replace('/feedback', '').strip()
    # Simpan umpan feedback dalam file teks
    log_feedback(message)
    bot.reply_to(message, "Thank you for your feedback!")
    log_user_message(message)

# Fungsi untuk memproses tugas yang dikirimkan pengguna
def process_assignment(file_path):
    return file_path

# Fungsi untuk menyimpan tugas yang telah diproses
def save_processed_assignment(file_path):
    processed_folder = "processed_assignments"
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
    new_file_path = os.path.join(processed_folder, os.path.basename(file_path))
    os.rename(file_path, new_file_path)
    return new_file_path

# Menangani pesan berupa foto atau dokumen yang dikirimkan pengguna
@bot.message_handler(content_types=['photo', 'document'])
def handle_files(message):
    # Ambil informasi tentang file yang dikirim
    file_info = bot.get_file(message.photo[-1].file_id if message.photo else message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = f"assignment_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg" if message.photo else f"assignment_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    # Simpan file ke dalam folder lokal
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f"Assignment file received and saved as {filename}")
    # Proses tugas dan kirimkan kembali
    processed_file_path = process_assignment(filename)
    new_filename = f"assignment_complete{os.path.splitext(filename)[1]}"
    processed_file = open(processed_file_path, 'rb')
    bot.send_document(message.chat.id, processed_file, caption=f"Here is your completed assignment hehe :)")
    processed_file.close()
    # Simpan tugas yang telah diproses
    save_processed_assignment(processed_file_path)
    log_user_message(message)

# Menjalankan bot agar selalu berjalan
while True:
    try:
        bot.polling()
    except Exception as e:
        print("Error:", e)
        # Jeda 1 detik sebelum menjalankan kembali bot
        time.sleep(1)