import os

# 配置類別，用於存放應用的配置設定
class Config:
    # 從環境變數中獲取 SECRET_KEY，用於加密和保護資料
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # 從環境變數中獲取資料庫的 URI 配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # 郵件伺服器設置
    MAIL_SERVER = 'smtp.googlemail.com'  # 郵件伺服器地址
    MAIL_PORT = 587  # 郵件伺服器的端口
    MAIL_USE_TLS = True  # 是否啟用 TLS 加密
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # 郵件帳號
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # 郵件帳號的密碼
