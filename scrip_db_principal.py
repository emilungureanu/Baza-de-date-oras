import sqlite3


conn = sqlite3.connect("db_informatii_principal.db")
c = conn.cursor()

# c.execute("CREATE TABLE persoane (id integer PRIMARY KEY, nume text, prenume text, telefon text, varsta text, adresa text, inaltime text, instagram text)")
# conn.commit()


c.execute("INSERT INTO persoane VALUES(NULL, 'Ungureanu', 'Emil', 'xxxx-xxx-xxx', '16', 'Exemplu Adresa', '180', 'emyu4')")
conn.commit()

c.execute("SELECT * FROM persoane")

for x in c.fetchall():
    print(x)