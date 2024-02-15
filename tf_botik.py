import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import tg_bot_token, open_weather_token
import logging


API_TOKEN = 'YOUR TOKEN'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start','main','hello'])
async def start_message(message: types.Message):
  await message.answer(f'Salom, {message.from_user.first_name},  Bizga ozingiz istagan joyning nomini yozing biz esa u yerdagi ob-havo malumotlarini sizga jonatamiz')


@dp.message_handler()
async def get_wather(message: types.Message):
    pass
    code_to_smile = {
        'Clear': 'Toza \U00002600',
        'Clouds': ' Bulutli \U00002601',
        'Rain': 'Yomgir \U00002614',
        'Thunderstorm': 'Boron \U000026A1',
        'Snow': 'Qor \U0001F328',
        'Mist': 'Tuman \U0001F32B',
    }
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        city = data['name']
        cur_weather = data['main']['temp']
        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Derazadan tashqariga qarang, men u erda ob-havo qandayligini tushunmayapman, odamlar u erda qanday qilib tirik?'

        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        await message.reply(f'''Погода в городе {city}
        Temperatura: {cur_weather}°C {wd}
        Shamol: {wind}м/с
        Namlik: {humidity}
        Kuningiz xayrli bo'lsin!''')
    except:
     await message.reply('\U00002620 Kiritilgan ism notogri. Iltimos, shahar nomini tekshiring \U00002620')
def main():
 city = input('Iltimos, shahar nomini kiriting. Keling, u erda ishlar qanday ketayotganini korib chiqaylik.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)