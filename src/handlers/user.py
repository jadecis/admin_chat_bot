from loader import dp, bot, html, db, y_pay
from config import YOOMONEY_WALLET
from yoomoney import Quickpay
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from src.keyboards.inline import product_menu, payment_menu
from datetime import datetime, date



@dp.message_handler(CommandStart(), state="*")
async def start_handler(msg: Message, state: FSMContext):
    if msg.chat.type == 'private':
        await state.finish()
        user= db.get_users(msg.chat.id)
        if user:
            db.up_username(msg.chat.username, msg.chat.id)
        else:
            db.add_user(
                user_id=msg.chat.id,
                username=msg.chat.username,
                date_reg=datetime.timestamp(datetime.now())
            )
        tar= db.get_tariffs()
        info= ""
        tar.pop(0)
        for i in tar:
            info+= f"<b>{i[1]} до {i[2]} в день и {i[3]} и в неделю за {i[4]}€/{i[5]}$/{i[6]}₽ в месяц.</b>\n"
            
        await msg.answer(f"Приветствую вас <b>{msg.chat.first_name}.</b>\n\n"
                        +f"<i>В нашем чате есть возможность платного продвижения объявления,"
                        +f"путем закрепления вашего рекламного объявления в шапке чата. Стоимость 10€/10$/800₽ в сутки.\n"
                        +f"Если вы исчерпали лимит бесплатных объявлений: 2 в день и 4 в неделю, вы можете увеличить лимит по одному из трех пакетов:</i>"
                        +f"\n{info}", parse_mode=html, reply_markup=product_menu(tar))
    
@dp.callback_query_handler(text= 'pin')
async def pin_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Для покупки «закрепа» в чате Черногория 🇲🇪 Объявления свяжитесь с админом @d_zak")


@dp.callback_query_handler(text_contains= 'prod_')
async def prod_hand(call: CallbackQuery, state: FSMContext):
    id= int(call.data.replace('prod_', ''))
    tar= db.get_tariffs(id=id)
    bill_id= str(call.message.chat.id) + str(tar[0]) 
    bill = Quickpay(
            receiver=YOOMONEY_WALLET,
            quickpay_form='shop',
            targets='Photo bot',
            paymentType='SB',
            sum=tar[6],
            label=bill_id)
    await call.message.edit_text(text=f"📍 <b>Счет для оплаты готов</b> 📍\n\n"
                            +f"<i>Для оплаты нажмите кнопку ниже 💳\n\n"
                            +f"<b>❗️ Счет действителен только 1 час</b> ❗️\n"
                            +f"После оплаты нажмите на кнопку «Проверить платеж», для проверки платежа</i>", 
                            reply_markup=payment_menu(url=bill.redirected_url, bill_id=bill_id),
                            parse_mode=html)
    
@dp.callback_query_handler(text_contains='checkbill_')
async def lot_hadler(call: CallbackQuery, state: FSMContext):
    bill_id= call.data.replace('checkbill_', '')
    tar= db.get_tariffs(id=int(bill_id.replace(f'{call.message.chat.id}', '')))
    history = y_pay.operation_history(label=bill_id)
    try:
        result= history.operations[-1]
        result=result.status
        if result== 'PAID' or result == 'success' or result == 'paid':
            db.edit_user_tar(
                user_id=call.message.chat.id,
                day=tar[2],
                week= tar[3]
            )
            try:
                db.add_subscriptions(
                    tariff_id=tar[0],
                    user_id=call.message.chat.id,
                    date=datetime.timestamp(datetime.today())
                )
            except Exception as ex:
                print(ex)
                db.up_subscriptions(
                    tariff_id=tar[0],
                    user_id=call.message.chat.id,
                    date=datetime.timestamp(datetime.today())
                )
            await call.message.edit_text(f"Оплата прошла успешно! Тариф повышен на {tar[1]}")
    except Exception as ex:
        print(ex)
        await bot.answer_callback_query(call.id, "❌ Оплата не прошла!\nПовторите попытку!", show_alert=True)

    