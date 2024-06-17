from flask import Flask
from extensions import jwt
from api.akun.endpoints import akun_endpoints
from api.data_wisata.endpoints import data_wisata_endpoints
from api.kategori.endpoints import kategori_endpoints
from api.profile.endpoints import profile_endpoints
from api.ulasan.endpoints import ulasan_endpoints
from api.wisata_favorit.endpoints import wisata_favorit_endpoints
from api.auth.endpoints import auth_endpoints
from static.static_file_server import static_file_server
from dotenv import load_dotenv
from flask_cors import CORS
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

jwt.init_app(app)

app.register_blueprint(akun_endpoints, url_prefix='/akun')
app.register_blueprint(data_wisata_endpoints, url_prefix='/data_wisata')
app.register_blueprint(kategori_endpoints, url_prefix='/kategori')
app.register_blueprint(profile_endpoints, url_prefix='/profile')
app.register_blueprint(ulasan_endpoints, url_prefix='/ulasan')
app.register_blueprint(wisata_favorit_endpoints, url_prefix='/wisata_favorit')
app.register_blueprint(auth_endpoints, url_prefix='/auth')
app.register_blueprint(static_file_server, url_prefix='/static/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
