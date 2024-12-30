from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# 定義一個 Blueprint，用於管理與用戶相關的路由
users = Blueprint('users', __name__)

# 用戶註冊路由
@users.route("/register", methods=['GET', 'POST'])
def register():
    # 如果用戶已經登入，則重定向到首頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()  # 建立註冊表單
    if form.validate_on_submit():  # 當表單通過驗證
        # 使用 bcrypt 加密密碼
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 創建新用戶並保存到資料庫
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('帳號已建立！現在可以登入了。', 'success')  # 顯示成功訊息
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# 用戶登入路由
@users.route("/login", methods=['GET', 'POST'])
def login():
    # 如果用戶已經登入，則重定向到首頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()  # 建立登入表單
    if form.validate_on_submit():
        # 根據電子郵件查找用戶
        user = User.query.filter_by(email=form.email.data).first()
        # 驗證用戶密碼
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # 設定登入狀態
            next_page = request.args.get('next')  # 檢查是否有重定向頁面
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('登入失敗，請檢查電子郵件與密碼是否正確。', 'danger')
    return render_template('login.html', title='Login', form=form)

# 用戶登出路由
@users.route("/logout")
def logout():
    logout_user()  # 清除登入狀態
    return redirect(url_for('main.home'))

# 用戶帳戶管理路由
@users.route("/account", methods=['GET', 'POST'])
@login_required  # 確保使用者登入
def account():
    form = UpdateAccountForm()  # 建立帳戶更新表單
    if form.validate_on_submit():
        if form.picture.data:  # 如果上傳了圖片
            picture_file = save_picture(form.picture.data)  # 儲存圖片
            current_user.image_file = picture_file  # 更新用戶頭像
        # 更新用戶名稱和電子郵件
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()  # 保存變更
        flash('帳戶已更新！', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # 預設載入用戶現有資訊
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # 加載用戶頭像
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# 查看指定用戶的文章
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # 獲取當前頁數
    user = User.query.filter_by(username=username).first_or_404()  # 查找用戶
    # 分頁顯示該用戶的文章，按日期降序排列
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

# 發送重設密碼請求
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # 如果用戶已登入，則重定向到首頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()  # 建立重設密碼表單
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # 查找用戶
        send_reset_email(user)  # 發送重設密碼的電子郵件
        flash('已發送電子郵件，請按照指示重設密碼。', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# 使用重設密碼的 Token
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # 如果用戶已登入，則重定向到首頁
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)  # 驗證 Token 是否有效
    if user is None:  # 如果 Token 無效或過期
        flash('這是一個無效或過期的連結。', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()  # 建立重設密碼表單
    if form.validate_on_submit():
        # 加密新密碼並更新到資料庫
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('密碼已更新！現在可以登入了。', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
