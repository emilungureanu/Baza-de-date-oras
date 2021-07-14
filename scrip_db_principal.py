import sqlite3


conn = sqlite3.connect("db_informatii_principal.db")
c = conn.cursor()

# c.execute("CREATE TABLE persoane (id integer PRIMARY KEY, nume text, prenume text, telefon text, varsta text, adresa text, inaltime text, instagram text, detalii text)")
# conn.commit()


c.execute("INSERT INTO persoane VALUES(NULL, 'Vasile', 'Emil', '0425698745', '16', 'Exemplu Adresa', '180', 'gigel.gigel', 'Ii place sa manance')")
conn.commit()

c.execute("SELECT * FROM persoane")

for x in c.fetchall():
    print(x)