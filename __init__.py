from flask import Flask
from datetime import timedelta

# import config

app = Flask(__name__, template_folder='templates', static_folder='statics', static_url_path='/static')
# app.config.from_object(config)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SECRET_KEY'] = "cmq"
app.config['UPLOAD_FOLDER '] = "sporting_goods/statics/images"

from app.WeChat import wechat

app.register_blueprint(wechat)
