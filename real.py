from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests

bot = Bot(token="token")
dp = Dispatcher(bot)

open_weather_token = 'token'

type_weather = {
    "Clear": "Ясно",
    "Clouds": "Облачно",
    "Rain": "Дождь",
    "Drizzle": "Дождь",
    "Thunderstorm": "Гроза",
    "Snow": "Снег ",
    "Mist": "Туман"
}


# Приветствие
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет!\n Этот бот показывает погоду в выбранном городе. Просто отправьте'
                                                 ' название города, а я расскажу, что Вам надеть :)')


@dp.message_handler(content_types=["text"])
async def do_something(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        temp = data['main']['temp'] # Температура

        # Проверяем, есть ли тип погоды в словаре
        wd = ""
        if data["weather"][0]["main"] in type_weather:
            wd = type_weather[data["weather"][0]["main"]]

        # Есть ли дождь или нет
        umbrl = ''
        if wd == 'Дождь':
            umbrl = 'и возьмите зонт'

        # Определяем по температуре, что нам нужно надевать
        if temp < 1:
            result = 'Наденьте теплую куртку'
        elif temp < 13:
            result = 'Холодно, наденьте куртку'
        elif temp < 17:
            result = 'Прохладно, лучше надеть худи'
        else:
            result = 'На улице тепло, надевай футболку'

        await bot.send_message(message.from_user.id, f"{result} {umbrl} ({data['main']['temp']}C° {wd})")

    except Exception as ex:
        await bot.send_message(message.from_user.id, "Проверьте название города")


executor.start_polling(dp)
