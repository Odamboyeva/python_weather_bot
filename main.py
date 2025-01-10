import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# WeatherAPI kalitingizni shu yerga qo'ying
API_KEY = 'b54a20ad99d94f9a9e8112022242211'

# Telegram bot API tokenini shu yerga qo'ying
TELEGRAM_API_TOKEN = "7861352874:AAEPCMtWHImZoqQHaYRb2YoiMwBypsJpMXk"

# WeatherAPI bilan ob-havo ma'lumotlarini olish
def get_weather_info(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        location = weather_data['location']['name']
        country = weather_data['location']['country']
        temperature = weather_data['current']['temp_c']  # Harorat (°C)
        humidity = weather_data['current']['humidity']  # Namlik (%)
        wind_speed = weather_data['current']['wind_kph']  # Shamol tezligi (km/h)
        condition = weather_data['current']['condition']['text']  # Havo sharoiti (masalan, "Cloudy")

        weather_info = (
            f"{location}, {country} davlatidagi hozirgi ob-havo:\n"
            f"Harorat 🌡: {temperature}°C\n"
            f"Namlik 💧: {humidity}%\n"
            f"Shamol tezligi 🌪 : {wind_speed} km/h\n"
            f"Sharoit 🌦: {condition}"
        )
        return weather_info
    else:
        return f" ❌ Xatolik yuz berdi 🙅‍♀️❗️: {response.status_code}"

# /start komandasi uchun callback
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu Aleykum! Ob-havo ma'lumotlarini bilish uchun Shahar yoki Davlat 🫧 nomini yuboring [shahar nomi].\nMasalan 👉: /temperature Dubai 🎗"
    )

# /temperature komandasi uchun callback
async def temperature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        city = " ".join(context.args)
        weather_info = get_weather_info(city)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Shahar🌇 nomini kiriting.\nMasalan: /temperature Tashkent🏤")

# Main function to start the bot
def main() -> None:
    # Application ni yaratish
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Dispatcher orqali komandalar uchun handlerlar qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("temperature", temperature ))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()