import asyncio
import logging
from aiogram import Dispatcher, types
from aiogram.filters.command import Command
import datetime as dt
from config import db_cur, db_conn, bot
import mvideo

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


def db_save(article, name, price, product_url, current_time):
    db_cur.execute("INSERT INTO products (article, name, price, url, last_update) VALUES (%s,%s,%s,%s,%s);",
                [article, name, price, product_url, current_time])
    db_conn.commit()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Кидай ссылку на товар из Мвидео.")


@dp.message(lambda message: message.text.startswith('http'))
async def process_url(message: types.Message):
    current_time = dt.datetime.now()
    url = message.text
    product_id = url.split('-')[-1]
    product = mvideo.get_product(product_id)
    db_save(product['article'], product['name'], product['price'], product['product_url'], current_time)
    await message.answer("Ваша URL добавлена в БД и отслеживается.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
