import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import datetime as dt
import psycopg2

conn = psycopg2.connect("dbname=parse user=postgres password = 25356256")
cur = conn.cursor()


def db_save(article, name, price, product_url, current_time):  # Запись в БД
    cur.execute("INSERT INTO products (article, name, price, url, last_update) VALUES (%s,%s,%s,%s,%s);",
                [article, name, price, product_url, current_time])
    conn.commit()


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6653377733:AAEFsiT06Y43K23KyeIqoB32PtmaIcoykwU")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Кидай ссылку на товар из Мвидео.")


@dp.message(lambda message: message.text.startswith('http'))
async def process_url(message: types.Message):
    current_time = dt.datetime.now()
    url = message.text
    product_id = url.split('-')[-1]
    url_name = f'https://www.mvideo.ru/bff/product-details?productId={product_id}'
    url_price = f'https://www.mvideo.ru/bff/products/prices?productIds={product_id}&isPromoApplied=true&addBonusRubles=true'
    cookies = {'MVID_CITY_ID': 'CityCZ_975', 'MVID_REGION_ID': '1', 'MVID_REGION_SHOP': 'S002',
               'MVID_TIMEZONE_OFFSET': '3'}
    response_price = requests.get(url=url_price, cookies=cookies).json()
    response = requests.get(url=url_name, cookies=cookies).json()
    article = response['body']['productId']
    name = response['body']['name']
    price = response_price['body']['materialPrices'][0]['price']['salePrice']
    product_url = f'https://www.mvideo.ru/products/{article}'
    db_save(article, name, price, product_url, current_time)
    await message.answer("Ваша URL добавлена в БД и отслеживается.")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
