import datetime as dt
import time
import requests
import psycopg2
from aiogram import Bot
import asyncio

conn = psycopg2.connect("dbname=parse user=postgres password = 25356256")
cur = conn.cursor()
bot = Bot(token="6653377733:AAEFsiT06Y43K23KyeIqoB32PtmaIcoykwU")

url_name = 'https://www.mvideo.ru/bff/product-details?productId=30066105'
url_price = 'https://www.mvideo.ru/bff/products/prices?productIds=30066105&isPromoApplied=true&addBonusRubles=true'
cookies = {'MVID_CITY_ID': 'CityCZ_975', 'MVID_REGION_ID': '1', 'MVID_REGION_SHOP': 'S002', 'MVID_TIMEZONE_OFFSET': '3'}

response_price = requests.get(url=url_price, cookies=cookies).json()
response = requests.get(url=url_name, cookies=cookies).json()

article = response['body']['productId']
name = response['body']['name']
price = response_price['body']['materialPrices'][0]['price']['salePrice']
product_url = f'https://www.mvideo.ru/products/{article}'
current_time = dt.datetime.now()


def db_find_old_product():  # Поиск записи где last_update больше часа назад
    one_hour_ago = dt.datetime.now() - dt.timedelta(hours=1)
    cur.execute("SELECT * FROM products WHERE last_update < %s;", [one_hour_ago])
    return cur.fetchone()


async def send_notification(url, old_price, new_price):
    await bot.send_message('437912785', f"Цена изменилась с {old_price} на {new_price}. Ссылка на товар: {url}")


while True:
    product = db_find_old_product()
    if product:
        url = product[3]
        old_price = product[2]
        url_price = product[5]
        response_price = requests.get(url=url_price, cookies=cookies).json()
        price = response_price['body']['materialPrices'][0]['price']['salePrice']
        current_time = dt.datetime.now()
        if old_price == price:
            cur.execute("UPDATE products SET last_update = %s;", [current_time])
            conn.commit()
        else:
            cur.execute("UPDATE products SET price = %s;", [price])
            cur.execute("UPDATE products SET last_update = %s;", [current_time])
            conn.commit()
            asyncio.run(send_notification(url, old_price, price))

    time.sleep(3600)

