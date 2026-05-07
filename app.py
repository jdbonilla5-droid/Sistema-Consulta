from flask import Flask, render_template, request, Response, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta"

#LOGIN
USER = "Denisse"
PASS = "101803"

# DATOS SIMULADOS USUARIOS
users = [
    {
        "nombre": "Valentina Simbaña",
        "email": "valesim@solidario.fin.ec",
        "user": "vsimbana"
    },
    {
        "nombre": "Ivan Bonilla",
        "email": "ivanbon@solidario.fin.ec",
        "user": "ibonilla"
    },
    {
        "nombre": "Pablo Calvache",
        "email": "pablocal@solidario.fin.ec",
        "user": "pcalvache"
    },
]

# DATOS SIMULADOS COMPUTADORAS
computers = [
    {
        "servidor": "PC-01",
        "DNS": "pc01.solidario.fin.ec",
        "SO": "Windows 10"
    },
    {
        "servidor": "PC-02",
        "DNS": "pc02.solidario.fin.ec",
        "SO": "Windows 11"
    },
    {
        "servidor": "SRV-01",
        "DNS": "srv01.solidario.fin.ec",
        "SO": "Windows Server"
    },
]


def search_data(search, search_type, attributes, users, computers):

    resultado2 = []

    # DEFINIR TIPO
    if search_type == "users":

        valid_attrs = ["nombre", "email", "user"]
        data = users

    else:

        valid_attrs = ["servidor", "DNS", "SO"]
        data = computers

    # SI NO SELECCIONA ATRIBUTOS
    if not attributes:
        attributes = valid_attrs
    else:
        attributes = [a for a in attributes if a in valid_attrs]
    if not search.strip():

        for item in data:
            filtered = {}
            for attr in attributes:
                if attr in item:
                    filtered[attr] = item[attr]
            resultado2.append(filtered)

        return resultado2, attributes


    search_values = search.split(";")

    # EVITAR DUPLICADOS
    resultado_duplicados = {}

    for value in search_values:

        value = value.strip().lower()

        # BUSQUEDA USUARIOS
        if search_type == "users":

            for u in users:

                if (
                    value in u["nombre"].lower() or
                    value in u["email"].lower() or
                    value in u["user"].lower()
                ):

                    resultado_duplicados[u["user"]] = u

        # BUSQUEDA COMPUTADORAS
        elif search_type == "computers":

            for c in computers:

                if (
                    value in c["servidor"].lower() or
                    value in c["DNS"].lower() or
                    value in c["SO"].lower()
                ):

                    resultado_duplicados[c["servidor"]] = c

    # FILTRAR ATRIBUTOS
    for item in resultado_duplicados.values():

        filtered = {}

        for attr in attributes:

            if attr in item:
                filtered[attr] = item[attr]

        resultado2.append(filtered)

    return resultado2, attributes


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

    return render_template(
        "login.html",
        message=message
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
def index():

    # VALIDAR LOGIN
    if "user" not in session:

        return redirect("/login")

    results = []
    columns = []
    message = ""


    if request.method == "POST":

        search = request.form.get("search", "").strip()

        search_type = request.form.get(
            "type",
            "users"
        )

        attributes = request.form.getlist(
            "attributes"
        )

        # EJECUTAR BUSQUEDA
        results, columns = search_data(
            search,
            search_type,
            attributes,
            users,
            computers
        )


        with open(
            "logs.txt",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"Usuario: {session['user']} | "
                f"Busqueda: {search if search else 'TODOS'} | "
                f"Tipo: {search_type} | "
                f"Fecha: {datetime.now()}\n"
            )

        # MENSAJES
        if not results:

            message = "No se encontraron resultados"

        else:

            message = (
                f"{len(results)} resultado(s) encontrado(s)"
            )

    return render_template(
        "index.html",
        results=results,
        columns=columns,
        message=message,
        data_json=json.dumps(results),
        columns_json=json.dumps(columns)
    )


@app.route("/export")
def export():

    data = request.args.get("data")
    columns = request.args.get("columns")

    if not data or not columns:

        return "No hay datos para exportar"

    results = json.loads(data)
    columns = json.loads(columns)

    # GENERAR CSV
    def generate():

        # COLUMNAS
        yield ",".join(columns) + "\n"

        # FILAS
        for row in results:

            yield ",".join(
                str(row.get(col, ""))
                for col in columns
            ) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment;filename=resultados.csv"
        }
    )

if __name__ == "__main__":

    app.run(debug=True)