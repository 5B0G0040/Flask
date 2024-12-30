from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flaskblog.users.forms import RegistrationForm, LoginForm

# 初始化 Flask 應用程式
app = Flask(__name__)

# 設定密鑰，用於會話加密
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# 設定資料庫 URI，這裡使用 SQLite 資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 初始化 SQLAlchemy，用於資料庫操作
db = SQLAlchemy(app)

# 定義 User 類別，對應資料庫中的 user 表格
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 用戶 ID，主鍵
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名，唯一且不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 用戶郵箱，唯一且不可為空
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 用戶頭像，預設為 'default.jpg'
    password = db.Column(db.String(60), nullable=False)  # 密碼
    posts = db.relationship('Post', backref='author', lazy=True)  # 與 Post 類別的關聯

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 定義 Post 類別，對應資料庫中的 post 表格
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 文章 ID，主鍵
    title = db.Column(db.String(100), nullable=False)  # 文章標題
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發佈日期
    content = db.Column(db.Text, nullable=False)  # 文章內容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 文章的作者（外鍵）

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# 模擬的部落格文章資料（實際上是從資料庫中獲取）
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# 路由：首頁，顯示所有文章
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

# 路由：關於頁面
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# 路由：註冊頁面，處理註冊表單
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # 創建註冊表單
    if form.validate_on_submit():  # 表單提交且驗證成功
        flash(f'Account created for {form.username.data}!', 'success')  # 顯示成功訊息
        return redirect(url_for('home'))  # 重定向到首頁
    return render_template('register.html', title='Register', form=form)

# 路由：登入頁面，處理登入表單
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # 創建登入表單
    if form.validate_on_submit():  # 表單提交且驗證成功
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':  # 簡單的帳號密碼驗證
            flash('You have been logged in!', 'success')  # 顯示登入成功訊息
            return redirect(url_for('home'))  # 重定向到首頁
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')  # 顯示錯誤訊息
    return render_template('login.html', title='Login', form=form)

# 主程序入口
if __name__ == '__main__':
    app.run(debug=True)
