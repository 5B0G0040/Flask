from flask import Blueprint, render_template

# 建立錯誤處理的藍圖 (Blueprint)
errors = Blueprint('errors', __name__)

# 當發生 404 錯誤時，渲染 404 錯誤頁面
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# 當發生 403 錯誤時，渲染 403 錯誤頁面
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# 當發生 500 錯誤時，渲染 500 錯誤頁面
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
