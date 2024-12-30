from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


# 用來載入使用者資料，Flask-Login 會使用這個函數來取得目前登入的使用者
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 使用者資料模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 使用者 ID，主鍵
    username = db.Column(db.String(20), unique=True, nullable=False)  # 使用者名稱，唯一且不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 使用者電子郵件，唯一且不可為空
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 使用者頭像檔案名稱，預設為 default.jpg
    password = db.Column(db.String(60), nullable=False)  # 使用者密碼
    posts = db.relationship('Post', backref='author', lazy=True)  # 使用者發表的文章，與 Post 之間建立關聯

    # 生成密碼重設的 token，默認過期時間為 30 分鐘
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)  # 使用 SECRET_KEY 和過期時間創建 Serializer
        return s.dumps({'user_id': self.id}).decode('utf-8')  # 返回編碼的 token

    # 驗證密碼重設的 token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])  # 使用 SECRET_KEY 創建 Serializer
        try:
            user_id = s.loads(token)['user_id']  # 解碼並提取 user_id
        except:
            return None  # 若解碼失敗或過期，返回 None
        return User.query.get(user_id)  # 返回對應的使用者

    def __repr__(self):
        # 顯示使用者的簡要信息
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# 文章資料模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 文章 ID，主鍵
    title = db.Column(db.String(100), nullable=False)  # 文章標題，不可為空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發佈日期，預設為當前時間
    content = db.Column(db.Text, nullable=False)  # 文章內容，不可為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 關聯的使用者 ID，外鍵

    def __repr__(self):
        # 顯示文章的簡要信息
        return f"Post('{self.title}', '{self.date_posted}')"
