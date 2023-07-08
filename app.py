from flask import Flask
from os import getenv
from dotenv import load_dotenv
from flask_cors import CORS
from db.database import init_db

# load environmets variables from `.env` file
load_dotenv('.env')

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = getenv('MONGO_URI')

app.config['MONGODB_SETTINGS'] = {
    'host': getenv('MONGO_URI')
}

# Connect to mongo
init_db(app)

# Import and register the users blueprint
from routes import users
app.register_blueprint(users.users_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)