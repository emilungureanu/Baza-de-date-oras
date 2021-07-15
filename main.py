from flask import Flask, sessions, url_for, redirect, render_template, request, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "miau"

#Pagina default care redirectioneaza pe login
@app.route("/")
def default():
    return redirect(url_for("login"))

#Pagina de login
@app.route("/login", methods = ["POST", "GET"])
def login():
    global user_input, parola_input, pin_input
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        conn = sqlite3.connect("db_user_parole.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users")


        user_input = request.form["user_input"]
        parola_input = request.form["parola_input"]
        pin_input = request.form["pin_input"]


        se_afla_in_baza_de_date = False


        for lista_informatie in c.fetchall():
            if user_input == lista_informatie[0] and parola_input == lista_informatie[1] and pin_input == lista_informatie[2]:
                se_afla_in_baza_de_date = True

        if se_afla_in_baza_de_date == True:
            session["user_input"] = user_input
            session["parola_input"] = parola_input
            session["pin_input"] = pin_input

            return redirect(url_for("alegere_cautare_adaugare"))
        else:
            return redirect(url_for("login"))

#Pagina logout
@app.route("/logout")
def logout():
    session.pop("user_input", None)
    session.pop("parola_input", None)
    session.pop("pin_input", None)
    flash("Ai fost delogat!")
    return redirect(url_for("login"))

           
#Pagina alegere cautare sau adaugare persoane
@app.route("/alegere_cautare_adaugare", methods= ["POST", "GET"])
def alegere_cautare_adaugare():
    if request.method == "GET":
        return render_template("alegere_adaugare_sau_vizionare.html")
    
    if request.method == "POST":
        if request.form.get("buton_cautare"):
            return redirect(url_for("cautare_database"))
        if request.form.get("buton_adaugare"):
            return redirect(url_for("adaugare_database"))
 
#Cautare in baza de date
@app.route("/cautare_database", methods = ["GET", "POST"])
def cautare_database():
    global content1
    conn = sqlite3.connect("db_informatii_principal.db")
    c = conn.cursor()

    if request.method == "GET":
        return render_template("cautare_database.html")

    if request.method == "POST":
        data_search_principal = request.form["search_principal"]

        if ' ' in data_search_principal:
            lista_cuvinte_salvate = data_search_principal.split()
            c.execute(f"SELECT * FROM persoane WHERE nume = '{lista_cuvinte_salvate[0].title() or lista_cuvinte_salvate[1].title()}' OR prenume = '{lista_cuvinte_salvate[0].title() or lista_cuvinte_salvate[1].title()}'")

        else:
            c.execute(f"SELECT * FROM persoane WHERE nume = '{data_search_principal.title()}' OR prenume = '{data_search_principal.title()}' OR telefon = '{data_search_principal}' OR instagram = '{data_search_principal}'")

        content1 = c.fetchall()

        #Pentru pagina persoana sa verifice cate persoane gaseste
        len_content = len(content1)

        if len_content == 1:
            return redirect(url_for("pagina_persoana"))
        else:
            return redirect(url_for("lista_persoane"))

#Pagina persoana cand ESTE o altercatie in baza de date
@app.route("/lista_persoane", methods = ["POST", "GET"])
def lista_persoane():
    if request.method == "GET":
        return render_template("lista_persoane.html", content = content1)

      
#Pagina cu butoane persoane cand NU este nicio altercatie in baza de date
@app.route("/informatii_persoana")
def pagina_persoana():
    return render_template("pagina_persoana.html", content = content1)


#------------------------------------------------Nu merge----------------------------------------------------
#Pagina informatie persoana cand ESTE o altercatie in baza de date
@app.route("/<nume_persoana>")
def pagina_persoana_lista(nume_persoana):
    conn = sqlite3.connect("db_informatii_principal.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM persoane WHERE nume = '{nume_persoana}' OR prenume = '{nume_persoana}'")
    return redirect(url_for("login"))

#De despartit numele inainte de al cauta
#------------------------------------------------------------------------------------------------------



#Adaugare in baza de date
@app.route("/adaugare_database", methods = ["POST", "GET"])
def adaugare_database():
    if request.method == "GET":
        return render_template("adaugare_database.html")

    if request.method == "POST":
        input_nume = request.form["input_nume"]
        input_prenume = request.form["input_prenume"]
        input_telefon = request.form["input_telefon"]
        input_varsta = request.form["input_varsta"]
        input_cartier = request.form["input_cartier"]
        input_instagram = request.form["input_instagram"]
        input_detalii = request.form["textarea-detalii"]
        

        conn = sqlite3.connect("db_informatii_principal.db")
        c = conn.cursor()

        c.execute(f"INSERT INTO persoane VALUES(NULL, '{input_nume}', '{input_prenume}', '{input_telefon}', '{input_varsta}', '{input_cartier}', '180', '{input_instagram}', '{input_detalii}')")
        conn.commit()
        return redirect(url_for("main"))



#Rulam programul flask
if __name__ == "__main__":
    app.run(debug=True)