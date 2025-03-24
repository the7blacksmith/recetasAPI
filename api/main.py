from flask import Flask
from routes import recipes

app = Flask(__name__)
app.register_blueprint(recipes)

@app.route("/")
def home():
    return "<h1>Bienvenido a la API de recetas en español</h1>"
if __name__ == "__main__":
    app.run(debug=True)