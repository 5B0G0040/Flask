from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# 初始化資料庫
db = SQLAlchemy()

# 初始化密碼加密工具
bcrypt = Bcrypt()

# 初始化用戶登入管理
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # 未登入用戶會被重定向到的登入路由
login_manager.login_message_category = 'info'  # 提示訊息的樣式分類

# 初始化電子郵件
mail = Mail()

# 應用工廠函式，動態建立 Flask 應用
def create_app(config_class=Config):
    app = Flask(__name__)  # 建立 Flask 應用
    app.config.from_object(config_class)  # 從指定的配置類中載入配置

    # 將擴展初始化並綁定到應用
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # 匯入 Blueprint 並註冊
    from flaskblog.users.routes import users  # 用戶相關路由
    from flaskblog.posts.routes import posts  # 文章相關路由
    from flaskblog.main.routes import main  # 主頁面相關路由
    from flaskblog.errors.handlers import errors  # 錯誤處理路由

    app.register_blueprint(users)  # 註冊用戶 Blueprint
    app.register_blueprint(posts)  # 註冊文章 Blueprint
    app.register_blueprint(main)  # 註冊主頁面 Blueprint
    app.register_blueprint(errors)  # 註冊錯誤處理 Blueprint

    return app  # 返回應用實例
