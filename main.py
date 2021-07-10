from flask import Flask, sessions, url_for, redirect, render_template, request, session
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

@app.route("/logout")
def logout():
         
                
#Pagina main
@app.route("/main")
def main():
    if "user_input" and "parola_input" and "pin_input" in session:
        return "ce faci"
    else:
        return redirect(url_for("login"))


#Rulam programul flask
if __name__ == "__main__":
    app.run(debug=True)