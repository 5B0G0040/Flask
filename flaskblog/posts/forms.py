from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# 定義文章表單類，用於處理文章的標題與內容
class PostForm(FlaskForm):
    # 文章標題欄位
    title = StringField(
        '標題',  # 標籤名稱
        validators=[DataRequired()]  # 驗證器：檢查此欄位是否為必填
    )
    
    # 文章內容欄位
    content = TextAreaField(
        '內容',  # 標籤名稱
        validators=[DataRequired()]  # 驗證器：檢查此欄位是否為必填
    )
    
    # 表單提交按鈕
    submit = SubmitField('Post')  # 按鈕文字顯示為 "Post"
