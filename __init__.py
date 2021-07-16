from flask import Flask, url_for, redirect, render_template, request, session, flash, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "miau"

#Icon norisor
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
        conn = sqlite3.connect("//var//www//webApp//webApp//db_user_parole.db")
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
    if "user_input" and "parola_input" and "pin_input" in session:

        if request.method == "GET":
            return render_template("alegere_adaugare_sau_vizionare.html")
        
        if request.method == "POST":
            if request.form.get("buton_cautare"):
                return redirect(url_for("cautare_database"))
            if request.form.get("buton_adaugare"):
                return redirect(url_for("adaugare_database"))

    else:
        return redirect(url_for("login"))
 
#Cautare in baza de date
@app.route("/cautare_database", methods = ["GET", "POST"])
def cautare_database():
    global content1
    conn = sqlite3.connect("//var//www//webApp//webApp//db_informatii_principal.db")
    c = conn.cursor()

    if "user_input" and "parola_input" and "pin_input" in session:

        if request.method == "GET":
            return render_template("cautare_database.html")

        if request.method == "POST":
            data_search_principal = request.form["search_principal"]

            if ' ' in data_search_principal:
                lista_cuvinte_salvate = data_search_principal.split()
                c.execute(f"SELECT * FROM persoane WHERE nume = '{lista_cuvinte_salvate[0].title()}' OR nume = '{lista_cuvinte_salvate[1].title()}' AND prenume = '{lista_cuvinte_salvate[0].title()}' OR prenume = '{lista_cuvinte_salvate[1].title()}'")

            else:
                c.execute(f"SELECT * FROM persoane WHERE nume = '{data_search_principal.title()}' OR prenume = '{data_search_principal.title()}' OR telefon = '{data_search_principal}' OR instagram = '{data_search_principal}'")

            content1 = c.fetchall()

            #Pentru pagina persoana sa verifice cate persoane gaseste
            len_content = len(content1)
            
            if len_content == 0:
                return render_template("persoana_negasita.html")
            if len_content == 1:
                return redirect(url_for("pagina_persoana"))
            else:
                return redirect(url_for("lista_persoane"))

    else:
        return redirect(url_for("login"))

#Pagina persoana cand ESTE o altercatie in baza de date
@app.route("/lista_persoane", methods = ["POST", "GET"])
def lista_persoane():
    if "user_input" and "parola_input" and "pin_input" in session:

        if request.method == "GET":
            return render_template("lista_persoane.html", content = content1)

    else:
        return redirect(url_for("login"))

#Pagina cu butoane persoane cand NU este nicio altercatie in baza de date
@app.route("/informatii_persoana")
def pagina_persoana():
    if "user_input" and "parola_input" and "pin_input" in session:
    
        return render_template("pagina_persoana.html", content = content1)

    else:
        return redirect(url_for("login"))


#Pagina informatie persoana cand ESTE o altercatie in baza de date
@app.route("/<nume_persoana>")
def pagina_persoana_lista(nume_persoana):
    if "user_input" and "parola_input" and "pin_input" in session:

        conn = sqlite3.connect("//var//www//webApp//webApp//db_informatii_principal.db")
        c = conn.cursor()
        lista_nume_despartit = nume_persoana.split("_")

        c.execute(f"SELECT * FROM persoane WHERE nume = '{lista_nume_despartit[0].title()}' AND prenume = '{lista_nume_despartit[1].title()}'")
        
        return render_template("pagina_persoana.html", content = c.fetchall())

    else:
        return redirect(url_for("login"))  

#Adaugare in baza de date
@app.route("/adaugare_database", methods = ["POST", "GET"])
def adaugare_database():
    if "user_input" and "parola_input" and "pin_input" in session:

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
            

            conn = sqlite3.connect("//var//www//webApp//webApp//db_informatii_principal.db")
            c = conn.cursor()

            c.execute(f"INSERT INTO persoane VALUES(NULL, '{input_nume}', '{input_prenume}', '{input_telefon}', '{input_varsta}', '{input_cartier}', '180', '{input_instagram}', '{input_detalii}')")
            conn.commit()
            return redirect(url_for("alegere_cautare_adaugare"))

    else:
        return redirect(url_for("login"))




#Rulam programul flask
if __name__ == "__main__":
    app.run(debug=True)
