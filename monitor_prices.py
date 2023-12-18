import datetime as dt
import time
import asyncio
from config import bot, db_conn, db_cur
import mvideo


def db_find_old_product():  # Поиск записи где last_update больше часа назад
    one_hour_ago = dt.datetime.now() - dt.timedelta(hours=1)
    db_cur.execute("SELECT * FROM products WHERE last_update < %s;", [one_hour_ago])
    return db_cur.fetchone()


async def send_notification(url, old_price, new_price):
    await bot.send_message('437912785', f"Цена изменилась с {old_price} на {new_price}. Ссылка на товар: {url}")


while True:
    product = db_find_old_product()
    if product:
        current_time = dt.datetime.now()
        price = mvideo.get_price(product)
        url = product[3]
        old_price = product[2]
        if old_price == price:
            db_cur.execute("UPDATE products SET last_update = %s;", [current_time])
            db_conn.commit()
        else:
            db_cur.execute("UPDATE products SET price = %s;", [price])
            db_cur.execute("UPDATE products SET last_update = %s;", [current_time])
            db_conn.commit()
            asyncio.run(send_notification(url, old_price, price))

    time.sleep(3600)
