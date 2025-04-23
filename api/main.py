from flask import Flask
from extensions import mail
from routes import recipes
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(recipes)
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] =  os.getenv("M_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("M_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("M_USERNAME")
print("USERNAME:", os.getenv("M_USERNAME"))
print("PASSWORD:", os.getenv("M_PASSWORD"), len(os.getenv("M_PASSWORD")))

mail.init_app(app)

@app.route("/")
def home():
    return "<h1>Bienvenido a la API de recetas en español</h1>"
if __name__ == "__main__":
    app.run(debug=True)