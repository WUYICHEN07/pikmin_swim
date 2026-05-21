from app import create_app
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
