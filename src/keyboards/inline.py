from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import dict_country, list_flag, db
import random

def captcha_menu(answer):
    markup= InlineKeyboardMarkup(row_width=3)
    flag= dict_country[answer]
    captha=[
        {flag : True},
        {list_flag[random.randint(0, len(list_flag)-1)] : False}, 
        {list_flag[random.randint(0, len(list_flag)-1)] : False},
    ]
    random.shuffle(captha)
    for i in captha:
        for k,v in i.items():
            markup.insert(
                InlineKeyboardButton(f'{k}', callback_data=f'capt_{v}'),
            )
    
    return markup

tariff_menu= InlineKeyboardMarkup(row_width=1)

tariff_menu.add(
    InlineKeyboardButton('Изменить тарифы', callback_data='tariff'),
    InlineKeyboardButton('Установить лимит', callback_data='custom'),
    InlineKeyboardButton('Обнулить лимит', callback_data=f'reset'),
    InlineKeyboardButton('Выгрузить статистику за неделю', callback_data='excel'),
)

def edit_tariffs():
    markup= InlineKeyboardMarkup(row_width=1)
    tar= db.get_tariffs()
    for i in tar:
        markup.add(
            InlineKeyboardButton(f'🔻 {i[1]}', callback_data=f'tar_{i[0]}')
        )
    markup.add(
        InlineKeyboardButton(f'➕ Добавить новый', callback_data=f'tar_new')
    )
    return markup

def limit_menu(id):
    markup= InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(f'🖊 Изменить дневной лимит', callback_data=f'limit_day_{id}'),
        InlineKeyboardButton(f'🖊 Изменить недельный лимит', callback_data=f'limit_week_{id}'),
        InlineKeyboardButton(f'✏️ Изменить название', callback_data=f'limit_name_{id}'),
        InlineKeyboardButton(f'✏️ Изменить цены', callback_data=f'limit_price_{id}'),
    )
    
    return markup

def product_menu(tar_list):
    markup= InlineKeyboardMarkup(row_width=1)
    
    for i in tar_list:
        markup.add(
            InlineKeyboardButton(f'Купить {i[1]}', callback_data=f'prod_{i[0]}')
        )
    markup.add(
        InlineKeyboardButton(f'Купить Закреп', callback_data=f'pin')
    )
    return markup

def currency_menu(id):
    markup= InlineKeyboardMarkup(row_width=1)
    tar= db.get_tariffs(id=id)
    markup.add(
        InlineKeyboardButton('Доллары $', callback_data=f'cur_dol{tar[5]}'),
        InlineKeyboardButton('Евро €', callback_data=f'cur_eu{tar[4]}'),
        InlineKeyboardButton('Рубли ₽', callback_data=f'cur_rub{tar[6]}'),
    )
    
    return markup

def payment_menu(url, bill_id):
    markup= InlineKeyboardMarkup()
    markup.insert(
    InlineKeyboardButton('💳 ОПЛАТИТЬ', url=url)
    )
    markup.add(
    InlineKeyboardButton('✅ Проверить платеж', callback_data='checkbill_'+ str(bill_id))
    )
    return markup