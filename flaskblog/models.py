from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

# 用於管理用戶登入狀態的函式
@login_manager.user_loader
def load_user(user_id):
    # 根據用戶 ID 查詢用戶對象，支援 Flask-Login
    return User.query.get(int(user_id))

# 用戶模型類，對應資料庫中的用戶表
class User(db.Model, UserMixin):
    # 定義用戶的資料欄位
    id = db.Column(db.Integer, primary_key=True)  # 唯一的用戶 ID
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名稱，必須唯一
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件，必須唯一
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 用戶頭像檔名
    password = db.Column(db.String(60), nullable=False)  # 加密後的密碼
    # 建立與文章的關聯關係
    posts = db.relationship('Post', backref='author', lazy=True)  # 一對多關係，關聯文章

    # 用於在調試或日誌中顯示用戶對象
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 文章模型類，對應資料庫中的文章表
class Post(db.Model):
    # 定義文章的資料欄位
    id = db.Column(db.Integer, primary_key=True)  # 唯一的文章 ID
    title = db.Column(db.String(100), nullable=False)  # 文章標題
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發佈日期，默認為當前時間
    content = db.Column(db.Text, nullable=False)  # 文章內容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 關聯的用戶 ID

    # 用於在調試或日誌中顯示文章對象
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
