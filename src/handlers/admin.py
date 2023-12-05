from loader import dp, db, Admin
from config import admin_ids
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from src.keyboards.inline import tariff_menu, edit_tariffs, limit_menu
from datetime import datetime
import xlsxwriter
import os

@dp.message_handler(commands=['admin'], state="*")
async def admin_handler(msg: Message, state: FSMContext):
    if msg.chat.type == 'private':
        await state.finish()
        if admin_ids.__contains__(msg.chat.id):
            await msg.answer('Админ панель', reply_markup=tariff_menu)
    
@dp.callback_query_handler(text='tariff')
async def tariff_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Выбери дальнейшее действие:", reply_markup=edit_tariffs())

@dp.callback_query_handler(text='custom')
async def custom_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Отправь @username пользователя:")
    await Admin.username.set()

@dp.callback_query_handler(text='reset')
async def custom_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Отправь @username пользователя:")
    await Admin.reset.set()

@dp.callback_query_handler(text='excel')
async def custom_handler(call: CallbackQuery, state: FSMContext):
    workbook = xlsxwriter.Workbook('stat.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(f'A1', 'user_id')
    worksheet.write(f'B1', 'username')
    worksheet.write(f'C1', 'posts')
    result= db.get_stats()
    for i, j in enumerate(result, start=2):
        worksheet.write(f'A{i}', j[1])
        worksheet.write(f'B{i}', j[2])
        worksheet.write(f'C{i}', j[4])

    workbook.close()
    await call.message.answer_document(document=open('stat.xlsx', 'rb') )
    os.remove('stat.xlsx')


@dp.message_handler(content_types=['text'], state=Admin.reset)
async def username_handler(msg: Message, state: FSMContext):
    inf= db.get_user_BYusername(msg.text)
    if inf:
        await state.update_data(id=inf[1])
    else:
        await msg.answer("Пользователь не найден! Повторите попытку!")

@dp.message_handler(content_types=['text'], state=Admin.cust_limit)
async def cust_limit_handler(msg: Message, state: FSMContext):
    try:
        limit= msg.text.split('/')
        day= int(limit[0])
        week= int(limit[1])
        data= await state.get_data()
        db.edit_user_tar(
            user_id=data.get('id'),
            day=day,
            week=week
        )
        try:
            db.add_subscriptions(
                user_id=data.get('id'),
                tariff_id=0,
                date=datetime.timestamp(datetime.now())
            )
        except Exception as ex:
            print(ex)
            db.up_subscriptions(
                user_id=data.get('id'),
                tariff_id=0,
                date=datetime.timestamp(datetime.now())
            )
            
        await msg.answer("Лимиты успешно изменены!")
        await state.finish()
    except Exception as ex:
        print(ex)
        await msg.answer("Ошибка ввода! Отправь целочисленный лимит!")
        
@dp.callback_query_handler(text_contains='tar_')
async def tar_handler(call: CallbackQuery, state: FSMContext):
    if call.data == 'tar_new':
        await call.message.edit_text('Введи название тарифа:')
        await Admin.name.set()
    else:
        id=int(call.data.replace('tar_', ''))
        tar= db.get_tariffs(id=id)
        await call.message.edit_text(f'Выбери что ты хочешь сделать с тарифом {tar[1]}:', reply_markup=limit_menu(id))
        
@dp.callback_query_handler(text_contains='limit_')
async def limit_handler(call: CallbackQuery, state: FSMContext):     
    if call.data.__contains__('limit_price'):
        id=int(call.data.replace('limit_price_', ''))
        await call.message.edit_text(f'Введи новые цены для тарифа в виде евро/доллары/рубли:\nПример: 10/10/800')
        await Admin.tar_price.set()
        
    elif call.data.__contains__('limit_name'):
        id=int(call.data.replace('limit_name_', ''))
        await call.message.edit_text(f'Введи новое название тарифа:')
        await Admin.tar_name.set()
        
    elif call.data.__contains__('limit_day'):
        id=int(call.data.replace('limit_day_', ''))
        await call.message.edit_text(f'Введи новый дневной лимит:')
        await Admin.tar_day.set()

    elif call.data.__contains__('limit_week'):
        id=int(call.data.replace('limit_week_', ''))
        await call.message.edit_text(f'Введи новый недельный лимит:')
        await Admin.tar_week.set()
        
    await state.update_data(id=id)
    
    
@dp.message_handler(content_types=['text'], state=Admin.tar_name)
async def name_handler(msg: Message, state: FSMContext):
    data= await state.get_data()
    db.edit_tariff(id=data.get('id'), name=msg.text)
    await msg.answer('Название успешно изменно', reply_markup=limit_menu(data.get('id')))
    await state.finish()
    
@dp.message_handler(content_types=['text'], state=Admin.tar_day)
async def name_handler(msg: Message, state: FSMContext):
    try:
        int(msg.text)
        data= await state.get_data()
        db.edit_tariff(id=data.get('id'), day=int(msg.text))
        await msg.answer('Дневной лимит успешно изменн', reply_markup=limit_menu(data.get('id')))
        await state.finish()
    except Exception as ex:
        print(ex)
        await msg.answer("Ошибка ввода! Отправь целочисленный лимит!")

    
        
@dp.message_handler(content_types=['text'], state=Admin.tar_week)
async def name_handler(msg: Message, state: FSMContext):
    try:
        int(msg.text)
        data= await state.get_data()
        db.edit_tariff(id=data.get('id'), week=int(msg.text))
        await msg.answer('Недельный лимит успешно изменн', reply_markup=limit_menu(data.get('id')))
        await state.finish()
    except:
        await msg.answer("Ошибка ввода! Отправь целочисленный лимит!")
    

@dp.message_handler(content_types=['text'], state=Admin.name)
async def name_handler(msg: Message, state: FSMContext):
    await state.update_data(name= msg.text)
    await msg.answer('Введи дневной лимит:')
    await Admin.day.set()
    
@dp.message_handler(content_types=['text'], state=Admin.day)
async def name_handler(msg: Message, state: FSMContext):
    try:
        int(msg.text)
        await state.update_data(day= int(msg.text))
        await msg.answer('Введи недельный лимит:')
        await Admin.week.set()
    except:
        await msg.answer("Ошибка ввода! Отправь целочисленный лимит!")
    
        
@dp.message_handler(content_types=['text'], state=Admin.week)
async def name_handler(msg: Message, state: FSMContext):
    try:
        int(msg.text)
        await state.update_data(week= int(msg.text))
        await msg.answer('Введи ценны в виде евро/доллары/рубли:\nПример: 10/10/800')
        await Admin.price.set()
    except:
        await msg.answer("Ошибка ввода! Отправь целочисленный лимит!")

@dp.message_handler(content_types=['text'], state=Admin.tar_price)
async def price_handler(msg: Message, state: FSMContext):
    try:
        prices= msg.text.split('/')
        dol= int(prices[0])
        eu= int(prices[1])
        rub= int(prices[2])
        data= await state.get_data()
        db.edit_tariff(id=data.get('id'), dol=dol, eu=eu, rub=rub)
        await msg.answer('Цены успешно изменены')
        await state.finish()
    except:
         await msg.answer("Ошибка ввода!")
   
        
@dp.message_handler(content_types=['text'], state=Admin.price)
async def price_handler(msg: Message, state: FSMContext):
    try:
        prices= msg.text.split('/')
        dol= int(prices[0])
        eu= int(prices[1])
        rub= int(prices[2])
        data= await state.get_data()
        db.add_tariff(
            name=data.get('name'),
            day=data.get('day'),
            week= data.get('week'),
            dol=dol,
            eu=eu,
            rub=rub
        )
        await msg.answer(f"Тариф {data.get('name')}\n"
                        +f"С дневным лимитом {data.get('day')}\n"
                        +f"С недельным лимитом {msg.text}\n"
                        +f"Цены: {eu}€/{dol}$/{rub}₽ в месяц\n\n"
                        +f"Успешно создан!\n")
        await state.finish()
    except Exception as ex:
        print(ex)
        await msg.answer("Ошибка ввода! Отправь целочисленный лимит!")