from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from telebot import TeleBot, types
import uvicorn
import threading
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

# ВАЖНО: позже сюда вставишь ngrok URL
WEBAPP_URL = "file:///Users/arturernandeslitvinov/PycharmProjects/ABN/Channels_market/web/index.html#"

bot = TeleBot(token, parse_mode="HTML")
app = FastAPI()

# Раздаём папку web как статику
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/")
def serve_page():
    return FileResponse("web/index.html")

# БОТ
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(
        text="Открыть мини-приложение",
        web_app=types.WebAppInfo(url=WEBAPP_URL)
    )
    kb.add(btn)

    bot.send_message(
        message.chat.id,
        "Нажми кнопку, чтобы открыть мини-приложение.",
        reply_markup=kb
    )

@bot.message_handler(content_types=['web_app_data'])
def process_webapp(message):
    data = message.web_app_data.data
    bot.send_message(message.chat.id, f"Получил данные:\n<code>{data}</code>")

# Запуск FastAPI в отдельном потоке
def run_server():
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.infinity_polling(skip_pending=True)
