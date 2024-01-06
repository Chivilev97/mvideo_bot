import asyncio
import logging
from aiogram import Dispatcher, types
from aiogram.filters.command import Command
import datetime as dt
from config import db_cur, db_conn, bot
import mvideo
import re

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


def db_save(article, name, price, product_url, current_time, user_id):
    db_cur.execute("INSERT INTO products (article, name, price, url, last_update, user_id) VALUES (%s,%s,%s,%s,%s,%s);",
                   [article, name, price, product_url, current_time, user_id])
    db_conn.commit()


def db_select_urls(tg_chat):
    db_cur.execute("SELECT id FROM users WHERE tg_chat = %s;", [tg_chat])
    id = db_cur.fetchone()
    db_cur.execute("SELECT url FROM products WHERE user_id = %s;", [id])
    result = db_cur.fetchall()
    urls = []
    for i in range(0, len(result)):
        urls.append(result[i][0])
    return urls


def db_del(url, user_id):
    db_cur.execute("DELETE FROM products WHERE url = %s and user_id = %s", [url, user_id])
    db_conn.commit()
    return db_cur.rowcount != 0


def db_find_user(tg_chat):
    db_cur.execute("SELECT tg_chat FROM users WHERE tg_chat = %s", [tg_chat])
    return db_cur.fetchone()


def db_create_user(tg_chat):
    db_cur.execute("INSERT INTO users (tg_chat) VALUES (%s)", [tg_chat])
    db_conn.commit()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    tg_chat = message.chat.id
    if not db_find_user(tg_chat):
        db_create_user(tg_chat)
    await message.answer("Привет! Кидай ссылку на товар из Мвидео.")


@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    tg_chat = message.chat.id
    urls = db_select_urls(tg_chat)
    if urls:
        await message.answer("\n".join(urls))
    else:
        await message.answer('Список пуст')


@dp.message(Command("del"))
async def cmd_del(message: types.Message):
    url = message.text.split(' ')[1]
    tg_chat = message.chat.id
    db_cur.execute("SELECT id FROM users WHERE tg_chat = %s;", [tg_chat])
    user_id = db_cur.fetchone()
    status = db_del(url, user_id)
    print(url)
    if status:
        await message.answer("Ваша url удалена.")
    else:
        await message.answer("Не удалось найти такую url.")


@dp.message(lambda message: message.text.startswith('http'))
async def process_url(message: types.Message):
    current_time = dt.datetime.now()
    url = message.text
    product_id = re.search('[0-9]+$', url).group()
    product = mvideo.get_product(product_id)
    tg_chat = message.chat.id
    db_cur.execute("SELECT id FROM users WHERE tg_chat = %s;", [tg_chat])
    user_id = db_cur.fetchone()
    db_save(product['article'], product['name'], product['price'], product['product_url'], current_time, user_id)
    await message.answer("Ваша URL добавлена и отслеживается.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

