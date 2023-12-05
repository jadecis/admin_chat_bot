import sqlite3
from datetime import datetime

class Database():
    
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    def add_user(self, user_id, username, date_reg):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, username, date_reg) VALUES (?, ?, ?)", (user_id, username, date_reg,))

    def get_user_BYusername(self, username):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users WHERE username= ?", (username, )).fetchone()

    def up_username(self, username, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET username= ? WHERE user_id=?", (username, user_id,))

    def del_user(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
 
    def link_check(self, date, user_id):
        with self.connection:
            res= self.cursor.execute("SELECT id FROM users WHERE -date_reg + ? >= 86400 and user_id= ?", (date, user_id, )).fetchall()
            return bool(len(res))
        
    def get_tariffs(self, id= None):
        with self.connection:
            if id:
                return self.cursor.execute("SELECT * FROM tariffs WHERE id= ?", (id, )).fetchone()
            else:
                return self.cursor.execute("SELECT * FROM tariffs").fetchall()
        
    def add_tariff(self, name, day, week, rub, eu, dol):
        with self.connection:
            self.cursor.execute("INSERT INTO tariffs (name, day, week, Rub, Euro, dollar) VALUES (?, ?, ?, ?, ?, ?)", (name, day, week, rub, eu, dol, ))
            
    def del_tariff(self, id):
        with self.connection:
            self.cursor.execute("DELETE FROM tariffs WHERE id= ?", (id, ))
            
    def edit_tariff(self, id, name=None, day=None, week=None, rub=None, eu=None, dol=None):
        with self.connection:
            if name:
                self.cursor.execute("UPDATE tariffs SET name= ? WHERE id= ?", (name, id,))
            elif day:
                self.cursor.execute("UPDATE tariffs SET day= ? WHERE id= ?", (day, id,))
            elif week:
                self.cursor.execute("UPDATE tariffs SET week= ? WHERE id= ?", (week, id,))
            elif rub:
                self.cursor.execute("UPDATE tariffs SET Rub= ?, Euro=?, dollar=?  WHERE id= ?", (rub, eu, dol, id, ))

    def get_users(self, user_id= None):
        with self.connection:
            if user_id:
                return self.cursor.execute("SELECT * FROM users WHERE user_id= ?", (user_id, )).fetchone()
            else:
                return self.cursor.execute("SELECT * FROM users").fetchall()
            
    def up_day(self, limit, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET day= ? WHERE user_id=?", (limit, user_id,))
            
    def up_week(self, limit, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET week= ? WHERE user_id=?", (limit, user_id,))
            
    def get_subscriptions(self):
        return self.cursor.execute("SELECT * FROM subscriptions").fetchall()
    
    def add_subscriptions(self, user_id, tariff_id, date):
        return self.cursor.execute("INSERT INTO subscriptions (user_id, tariff_id, date) VALUES (?, ?, ?)", (user_id, tariff_id, date,))

    def up_subscriptions(self, user_id, tariff_id, date):
        return self.cursor.execute("UPDATE subscriptions SET tariff_id= ?, date= ? WHERE user_id=?", (tariff_id, date, user_id, ))

    def del_sub(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM subscriptions WHERE user_id= ?", (user_id, ))
            
    def reset_tariff(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET week= 4, day= 2 WHERE user_id=?", ( user_id,))
            
    def new_post(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET week=week - 1, day= day -1 WHERE user_id=?", ( user_id,))
            
    def edit_user_tar(self, user_id, day, week):
        with self.connection:
            self.cursor.execute("UPDATE users SET day= ?, week=? WHERE user_id= ?", (day, week, user_id,))
            
    # def custom_tar(self, user_id, day, week):
    #     with self.connection:
    #         self.cursor.execute("INSERT INTO custom (user_id, day, week) VALUES (?, ?, ?)", (user_id, day, week, ))
            
    # def get_custom_tar(self, user_id):
    #     with self.connection:
    #         return self.cursor.execute("SELECT * FROM custom WHERE user_id= ?", (user_id, )).fetchone()
            
    # def edit_custom_tar(self, user_id, day, week):
    #     with self.connection:
    #         self.cursor.execute("UPDATE custom SET day= ?, week= ? WHERE user_id= ?", (day, week, user_id,))
            
    def add_msg(self, msg_id, chat_id, date):
        with self.connection:
            self.cursor.execute("INSERT INTO deleter (msg_id, chat_id, date) VALUES (?, ?, ?)", (msg_id, chat_id, date,))
            
    def del_msg(self, msg_id):
        with self.connection:
            self.cursor.execute("DELETE FROM deleter WHERE msg_id= ?", (msg_id, ))
            
    def get_msg(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM deleter").fetchall()
        
    def add_posts(self, user_id, username, day=None, week=None):
        with self.connection:
            if day and week:
                self.cursor.execute("INSERT INTO stats (user_id, username, day, week) VALUES (?, ?, ?, ?)", (user_id, username, day, week, ))
            else:
                self.cursor.execute("INSERT INTO stats (user_id, username) VALUES (?, ?)", (user_id, username,))
            
    def up_posts(self, user_id, username):
        with self.connection:
            self.cursor.execute("UPDATE stats SET week=week+1, day=day+1, username= ? WHERE user_id= ? ", (username, user_id, ))
            
    def reset_posts(self, week= False):
        with self.connection:
            if week:
                self.cursor.execute("UPDATE stats SET week=0")
            else:
                self.cursor.execute("UPDATE stats SET day=0 ")
                
    def get_stats(self, user_id=None):
        with self.connection:
            if user_id:
                return self.cursor.execute("SELECT * FROM stats WHERE user_id= ?", (user_id, )).fetchone()
            else:
                return self.cursor.execute("SELECT * FROM stats").fetchall()
            
    def add_newUser(self, user_id, chat_id, msg_id):
        with self.connection:
            self.cursor.execute("INSERT INTO new (user_id, chat_id, date, msg_id) VALUES (?, ?, ?, ?)", (user_id, chat_id, datetime.timestamp(datetime.now()), msg_id, ))
            
    def get_newUsers(self, user_id=None):
        with self.connection:
            if user_id:
                return self.cursor.execute("SELECT * FROM new WHERE user_id= ?", (user_id, )).fetchone()
            return self.cursor.execute("SELECT * FROM new").fetchall()
        
    def delete_newUser(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM new WHERE user_id= ?", (user_id, ))