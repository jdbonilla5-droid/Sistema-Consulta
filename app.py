from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Proyecto funcionando"

app.run(debug=True)