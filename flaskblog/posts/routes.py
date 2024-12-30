from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# 定義 Blueprint，用於管理文章相關的路由
posts = Blueprint('posts', __name__)

# 新增文章路由
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required  # 確保只有登入用戶可以訪問
def new_post():
    form = PostForm()  # 使用 PostForm 表單
    if form.validate_on_submit():  # 如果表單驗證通過
        # 建立新文章，將當前用戶設為作者
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)  # 將文章添加到資料庫
        db.session.commit()  # 提交更改
        flash('您的文章已成功建立！', 'success')  # 顯示成功訊息
        return redirect(url_for('main.home'))  # 重定向到主頁
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')  # 顯示新文章表單

# 顯示單篇文章的路由
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  # 根據文章 ID 查詢，找不到則返回 404
    return render_template('post.html', title=post.title, post=post)  # 顯示文章詳情

# 更新文章路由
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required  # 確保只有登入用戶可以訪問
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # 根據文章 ID 查詢
    if post.author != current_user:  # 確保只有作者可以更新文章
        abort(403)  # 返回 403 禁止訪問錯誤
    form = PostForm()  # 使用 PostForm 表單
    if form.validate_on_submit():  # 如果表單驗證通過
        post.title = form.title.data  # 更新文章標題
        post.content = form.content.data  # 更新文章內容
        db.session.commit()  # 提交更改
        flash('您的文章已更新！', 'success')  # 顯示成功訊息
        return redirect(url_for('posts.post', post_id=post.id))  # 重定向到文章詳情頁
    elif request.method == 'GET':  # 如果是 GET 請求，預填充現有數據
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')  # 顯示更新文章表單

# 刪除文章路由
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required  # 確保只有登入用戶可以訪問
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # 根據文章 ID 查詢
    if post.author != current_user:  # 確保只有作者可以刪除文章
        abort(403)  # 返回 403 禁止訪問錯誤
    db.session.delete(post)  # 從資料庫刪除文章
    db.session.commit()  # 提交更改
    flash('您的文章已刪除！', 'success')  # 顯示成功訊息
    return redirect(url_for('main.home'))  # 重定向到主頁
