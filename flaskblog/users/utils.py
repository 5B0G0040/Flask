import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# 儲存用戶上傳的頭像圖片
def save_picture(form_picture):
    # 生成隨機檔名以避免檔案名稱衝突
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # 分離檔名與副檔名
    picture_fn = random_hex + f_ext  # 生成新檔案名稱
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # 定義儲存路徑

    # 調整圖片大小
    output_size = (125, 125)  # 設定輸出的圖片大小為 125x125 像素
    i = Image.open(form_picture)  # 開啟圖片
    i.thumbnail(output_size)  # 調整縮略圖大小
    i.save(picture_path)  # 儲存縮放後的圖片

    return picture_fn  # 返回新生成的檔案名稱

# 發送重設密碼的電子郵件
def send_reset_email(user):
    # 生成用戶的密碼重設 Token
    token = user.get_reset_token()
    # 建立電子郵件內容
    msg = Message('Password Reset Request',  # 主旨
                  sender='noreply@demo.com',  # 寄件人
                  recipients=[user.email])  # 收件人清單（用戶的電子郵件地址）
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}  # 密碼重設的連結

If you did not make this request then simply ignore this email and no changes will be made.
（如果這不是您發出的請求，請忽略此郵件，密碼將不會有任何更動。）
'''
    mail.send(msg)  # 使用 Flask-Mail 發送電子郵件
