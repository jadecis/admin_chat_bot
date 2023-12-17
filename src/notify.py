from loader import db, bot
from datetime import datetime
from dateutil.relativedelta import relativedelta
import asyncio
import aioschedule

async def everyday():
    db.reset_posts()
        
async def everyweek():
    db.reset_posts(week=True)

async def everysub():
    sub= db.get_subscriptions()
    for i in sub:
        sub_date= datetime.fromtimestamp(i[2]) + relativedelta(months=+1)
        if sub_date < datetime.today():
            db.del_sub(i[0])
            db.reset_tariff(i[0])


async def delete_message():
    inf= db.get_msg()
    if inf:
        for i in inf:
            if -i[2] + datetime.timestamp(datetime.now()) >= 0:
                try:
                    await bot.delete_message(
                        chat_id=i[1],
                        message_id=i[0],
                    )    
                except:
                    continue   
                db.del_msg(i[0])  
    
async def ban_user():
    result= db.get_newUsers()
    if result:
        for i in result:
            if i[3] <= datetime.timestamp(datetime.now()):
                try: await bot.ban_chat_member(chat_id=i[2], user_id=i[1])
                except: pass
                try: await bot.delete_message(chat_id=i[2], message_id=i[4])       
                except: pass
                db.delete_newUser(i[1])

async def scheduler():
    aioschedule.every().day.at('00:10').do(everysub)
    aioschedule.every().day.at("00:00").do(everyday)
    aioschedule.every().monday.at('00:01').do(everyweek)
    aioschedule.every().minute.do(delete_message)
    aioschedule.every(30).seconds.do(ban_user)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)