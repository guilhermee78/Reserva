from flask import Flask
from sql import db
from reserva_controler import routes
from config import Config  

app = Flask(__name__)
app.config.from_object(Config) 

db.init_app(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)