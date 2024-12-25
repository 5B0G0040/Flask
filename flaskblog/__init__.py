from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# 設定 secret key
app.config['SECRET_KEY'] = 'your_secret_key'

# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# 初始化資料庫
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 初始化 login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 登入頁面
login_manager.login_message_category = 'info'

# 用戶加載方法
from flaskblog.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flaskblog import routes
