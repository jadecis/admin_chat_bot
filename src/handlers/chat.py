from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot, html, list_country
from src.keyboards.inline import captcha_menu 
from datetime import datetime, timedelta
import random


# @dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS)
# async def chat_handler(msg: Message):
#     index= random.randint(0, 6)
#     for k, v in list_country[index].items():
#         country= k
#     await msg.answer(text=f"Выберите флаг {country}", reply_markup= captcha_menu(country))
   
@dp.chat_member_handler()
async def some_handler(msg: ChatMemberUpdated):
    if msg.new_chat_member.status == 'member' :
        name= f"@{msg.new_chat_member.user.username}" if msg.new_chat_member.user.username else msg.new_chat_member.user.full_name
        index= random.randint(0, 5)
        for k, v in list_country[index].items():
            country= k
        message= await bot.send_message(chat_id= msg.chat.id, text=f"Привет, {name}!\n\nВыберите флаг {country}", reply_markup= captcha_menu(country))
        db.add_newUser(user_id=msg.new_chat_member.user.id,
                       chat_id=msg.chat.id,
                       msg_id=message.message_id)


@dp.channel_post_handler()
@dp.message_handler(content_types=['text', 'photo', 'video'])
async def message_handler(msg: Message):
    if msg.chat.type == 'supergroup' or msg.chat.type == 'group':
        if not(db.get_users(user_id=msg.from_user.id)):
            await msg.delete()
            if db.get_newUsers(msg.from_user.id): return
            name= f"@{msg.from_user.username}" if msg.from_user.username else msg.from_user.user.full_name
            index= random.randint(0, 5)
            for k, v in list_country[index].items():
                country= k
            message= await bot.send_message(chat_id= msg.chat.id, text=f"Привет, {name}!\n\nВыберите флаг {country}", reply_markup= captcha_menu(country))
            db.add_newUser(user_id=msg.from_user.id,
                        chat_id=msg.chat.id,
                        msg_id=message.message_id)
        else:
            limits=db.get_users(user_id=msg.from_user.id)
            user= db.get_stats(msg.from_user.id)
            name= msg.from_user.username if msg.from_user.username else msg.from_user.full_name
            if user[3] < limits[4] and user[4] < limits[5]:
                if msg.text:
                    if msg.text.__contains__('https://'):
                        if not(db.link_check(date=datetime.timestamp(datetime.now()),
                                user_id=msg.from_user.id)):
                            await msg.delete()
                    else:
                        db.up_posts(msg.from_user.id, name)
                elif msg.caption:
                    if msg.caption.__contains__('https://'):
                        if not(db.link_check(date=datetime.timestamp(datetime.now()),
                                    user_id=msg.from_user.id)):
                            await msg.delete()
                    else:
                        db.up_posts(msg.from_user.id, name)
            else:
                await msg.delete()
                if msg.text or msg.caption:
                    info_bot= await bot.get_me()
                    msg_id= await msg.answer(f"Уважаемый пользователь <b>{msg.from_user.first_name}</b>, "
                                    +f"вы превысили лимит на размещение объявлений, все сообщения"
                                    +f" сверх лимита будут удаляться  {hlink('правила', f'https://t.me/montenegro_ads/13748')}. "
                                    +f"Если вы хотите узнать больше о дополнительных возможностях "
                                    +f"для публикации или платного размещения нажмите {hlink('здесь', f'https://t.me/{info_bot.username}?start')}.", parse_mode=html)
                    db.add_msg(
                        msg_id=msg_id.message_id,
                        chat_id=msg.chat.id,
                        date=datetime.timestamp(datetime.now()+timedelta(minutes=1))
                    )

@dp.callback_query_handler(text_contains='capt_')
async def capt_handler(call: CallbackQuery):
    await call.message.delete()
    db.delete_newUser(call.from_user.id)
    if call.data == 'capt_True':
        try:
            db.add_user(
                    user_id=call.from_user.id,
                    username=call.from_user.username,
                    date_reg=datetime.timestamp(datetime.now())
                )
        except:
            pass
    else:
        db.del_user(call.from_user.id)
        await bot.ban_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id)