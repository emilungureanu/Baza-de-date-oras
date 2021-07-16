import sqlite3


conn = sqlite3.connect("db_informatii_principal.db")
c = conn.cursor()

c.execute("CREATE TABLE persoane (id integer PRIMARY KEY, nume text, prenume text, telefon text, varsta text, adresa text, inaltime text, instagram text, detalii text)")
conn.commit()


# c.execute("INSERT INTO persoane VALUES(NULL, 'Mustea', 'David', '0425698333', '17', 'Exemplu Adresa 1', '182', 'george.george', 'Ii place sa bea')")
# conn.commit()

# lista = ["David", "Mustea"]
# c.execute(f"SELECT * FROM persoane WHERE nume = '{lista[0] or lista[1]}' AND prenume = '{lista[0] or lista[1]}'")

c.execute("SELECT * FROM persoane")

for x in c.fetchall():
    print(x)