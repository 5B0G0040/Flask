from flask import render_template, request, Blueprint
from flaskblog.models import Post

# 定義 Blueprint，用於管理主頁面和關於頁面的路由
main = Blueprint('main', __name__)

# 主頁面路由
@main.route("/")
@main.route("/home")
def home():
    # 獲取查詢參數中的頁碼，預設為第 1 頁
    page = request.args.get('page', 1, type=int)
    # 查詢文章，按發佈日期降序排列，並進行分頁（每頁顯示 5 篇文章）
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # 渲染主頁模板，將分頁的文章列表傳遞給模板
    return render_template('home.html', posts=posts)

# 關於頁面路由
@main.route("/about")
def about():
    # 渲染關於頁面的模板，並傳遞頁面標題
    return render_template('about.html', title='About')
