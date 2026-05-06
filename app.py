from flask import Flask, render_template, request, Response, redirect, session
import json
from datetime import datetime
from services.service import search_data

app = Flask(__name__)
app.secret_key = "clave_secreta"

USER = "Denisse"
PASS = "101803"

#Datos simulados
users = [
    {"nombre": "Valentina Simbaña", "email": "valesim@solidario.fin.ec", "user": "vsimbana"},
    {"nombre": "Ivan Bonilla", "email": "ivanbon@solidario.fin.ec", "user": "ibonilla"},
    {"nombre": "Pablo Calvache", "email": "pablocal@solidario.fin.ec", "user": "pcalvache"},
]

computers = [
    {"nombre_servidor": "PC-01", "DNS": "pc01.solidario.fin.ec", "SO": "Windows 10"},
    {"nombre_servidor": "PC-02", "DNS": "pc02.solidario.fin.ec", "SO": "Windows 11"},
    {"nombre_servidor": "SRV-01", "DNS": "srv01.solidario.fin.ec", "SO": "Windows Server"},
]

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER and password == PASS:
            session["user"] = username
            return redirect("/")
        else:
            message = "Credenciales incorrectas"

    return render_template("login.html", message=message)

#LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#INDEX
@app.route("/", methods=["GET", "POST"])
def index():

    #ingreso solo usuarios logeados
    if "user" not in session:
        return redirect("/login")

    results = []
    columns = []
    message = ""

    if request.method == "POST":
        search = request.form.get("search", "").strip()
        search_type = request.form.get("type", "users")
        attributes = request.form.getlist("attributes")

        #evita busquedas vacias
        if not search:
            message = "Ingrese un valor para buscar"
            return render_template(
                "index.html",
                results=[],
                columns=[],
                message=message,
                data_json="[]",
                columns_json="[]"
            )

        results, columns = search_data(
            search,
            search_type,
            attributes,
            users,
            computers
        )

        #LOGGING
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(
                f"Usuario: {session['user']} | "
                f"Busqueda: {search} | "
                f"Tipo: {search_type} | "
                f"Fecha: {datetime.now()}\n"
            )

        if not results:
            message = "No se encontraron resultados"
        else:
            message = f"{len(results)} resultado(s) encontrado(s)"

    #renderizacion
    return render_template(
        "index.html",
        results=results,
        columns=columns,
        message=message,
        data_json=json.dumps(results),
        columns_json=json.dumps(columns)
    )

#Exportacion scv
@app.route("/export")
def export():
    data = request.args.get("data")
    columns = request.args.get("columns")

    if not data or not columns:
        return "No hay datos para exportar"

    results = json.loads(data)
    columns = json.loads(columns)

    def generate():
        yield ",".join(columns) + "\n"
        for row in results:
            yield ",".join(str(row.get(col, "")) for col in columns) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=resultados.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)