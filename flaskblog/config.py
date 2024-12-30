import os

# 配置類，用於管理應用的配置參數
class Config:
    # 安全金鑰，用於防止 CSRF 攻擊，並用於其他安全相關功能
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    
    # 資料庫連結，支援從環境變數讀取（方便在不同環境中部署）
    # 默認使用 SQLite 資料庫
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    
    # 電子郵件伺服器設定
    MAIL_SERVER = 'smtp.googlemail.com'  # 電子郵件伺服器地址，這裡以 Gmail 為例
    MAIL_PORT = 587  # 電子郵件伺服器連接埠，587 用於 TLS 加密
    MAIL_USE_TLS = True  # 啟用傳輸層安全性協定 (TLS)

    # 電子郵件帳號認證（從環境變數讀取，提升安全性）
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # 發送郵件的電子郵件帳號
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # 對應的電子郵件密碼
