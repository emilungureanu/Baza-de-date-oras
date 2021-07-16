import sqlite3


conn = sqlite3.connect("db_user_parole.db")
c = conn.cursor()

# c.execute("CREATE TABLE users (user text, parola text, pin text)")
# conn.commit()


# c.execute("INSERT INTO users VALUES('emil_ungureanu', 'Milsugi1', '458-423')")
# conn.commit()

c.execute("SELECT * FROM users")

for x in c.fetchall():
    print(x)