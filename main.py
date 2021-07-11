import re
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

            return redirect(url_for("main"))
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
              
#Pagina main unde alegi baza de date sau intrebari
@app.route("/main", methods = ["GET", "POST"])
def main():
    if "user_input" and "parola_input" and "pin_input" in session:
        if request.method == "GET":
            return render_template("index.html")


        if request.method == "POST":
            if request.form.get("buton_baza_de_date"):
                return redirect(url_for("alegere_cautare_adaugare"))

            if request.form.get("buton_intrebari"):
                return "salut" # de pus intrebari

                    
    else:
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
    if request.method == "GET":
        return render_template("cautare_database.html")
    if request.method == "POST":
        data_search_principal = request.form["search_principal"]
#Adaugare in baza de date
@app.route("/adaugare_database")
def adaugare_database():
    return render_template("adaugare_database.html")


#Rulam programul flask
if __name__ == "__main__":
    app.run(debug=True)