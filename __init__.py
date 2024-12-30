from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# 初始化擴展套件
db = SQLAlchemy()  # 用於資料庫操作
bcrypt = Bcrypt()  # 用於密碼加密
login_manager = LoginManager()  # 用於管理使用者登入
login_manager.login_view = 'users.login'  # 設定當用戶未登入時重定向的路由
login_manager.login_message_category = 'info'  # 設定登入訊息的顯示類別
mail = Mail()  # 用於發送郵件

# 創建並配置 Flask 應用
def create_app(config_class=Config):
    app = Flask(__name__)  # 創建 Flask 應用實例
    app.config.from_object(Config)  # 讀取配置

    # 初始化各種擴展
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # 註冊藍圖（Blueprints）
    from flaskblog.users.routes import users  # 引入使用者路由
    from flaskblog.posts.routes import posts  # 引入文章路由
    from flaskblog.main.routes import main  # 引入主頁面路由
    from flaskblog.errors.handlers import errors  # 引入錯誤處理路由

    # 註冊各藍圖
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
