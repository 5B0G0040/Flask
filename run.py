from flaskblog import create_app

# 創建 Flask 應用實例
app = create_app()

# 如果是直接執行此文件，啟動 Flask 開發伺服器
if __name__ == '__main__':
    app.run(debug=True)  # 開啟調試模式，便於開發時即時看到錯誤資訊
