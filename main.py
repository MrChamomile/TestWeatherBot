import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message

from APIs import OpenWeatherApi, TelegramApi



async def get_temperature(city_name, api_key=OpenWeatherApi):
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

	response = requests.get(url)

	if response.status_code == 200:
		data = response.json()

		temperature = data["main"]["temp"]
		humidity = data["main"]["humidity"]
		weather = data["weather"][0]["description"]

		return f"temperature: {temperature}\nhumidity: {humidity}\nweather: {weather}"
	else:
		return f"error: {response.status_code}"



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TelegramApi)

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello! You in this bot you can get valid temperature in any city.\nJust send me name of it")

@dp.message()
async def show_weather(message: Message):
	weather = await get_temperature(message.text)
	await bot.send_message(message.from_user.id, weather)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())