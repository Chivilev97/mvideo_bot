import os
import psycopg2
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()
db_conn = psycopg2.connect(os.environ['DB_CONNECTION_STRING'])
db_cur = db_conn.cursor()
bot = Bot(token=os.environ['BOT_TOKEN'])
