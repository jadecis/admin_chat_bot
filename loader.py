from aiogram import Bot, Dispatcher, types
from src.database.db import Database
from config  import TOKEN_BOT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from freekassa import FreeKassaApi
from aiogram.dispatcher.filters.state import StatesGroup, State
from yoomoney import Client
from config import YOOMONEY_TOKEN, YOOMONEY_WALLET
import logging

bot = Bot(token=TOKEN_BOT)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot, storage=MemoryStorage())
html= types.ParseMode.HTML #<- &lt; >- &gt; &- &amp;
db= Database('src/database/database.db')
y_pay = Client(YOOMONEY_TOKEN)

# client = FreeKassaApi(
#     first_secret='5w,_wYjTT2zh=I{',
#     second_secret='lXiIdg+5xQnq]3v',
#     merchant_id=2396,
#     wallet_id=0,
#     wallet_api_key='24b3d1a83b7abf8580630fc15bfaa476')

list_country= [{'Черногории' : '🇲🇪' } , {'Сербии' : '🇷🇸'}, {'Хорватии' : '🇭🇷'},
               {'Боснии и Герцоговины' : '🇧🇦'}, {'Македонии' : '🇲🇰'}, {'Словении' : '🇸🇮'}]

list_flag= ['🇦🇫', '🇦🇱', '🇦🇶', '🇩🇿', '🇲🇽', '🇾🇪', '🇸🇷', '🇸🇪', '🇵🇭', '🇸🇳', '🇷🇺']

dict_country= {
    'Черногории' : '🇲🇪',
    'Сербии' : '🇷🇸',
    'Хорватии' : '🇭🇷',
    'Боснии и Герцоговины' : '🇧🇦',
    'Македонии' : '🇲🇰',
    'Косово' : '🇽🇰',
    'Словении' : '🇸🇮'}

class Admin(StatesGroup):
    name= State()
    day= State()
    week= State()
    price= State()
    tar_price= State()
    tar_name= State()
    tar_day= State()
    tar_week= State()
    username= State()
    reset= State()
    cust_limit= State()