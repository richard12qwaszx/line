import os
import json

# 引入套件
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

# 我們使用 Google API 的範圍為 spreadsheets
gsp_scopes = ['https://spreadsheets.google.com/feeds']

# 讀入環境變數參數
SPREAD_SHEETS_KEY = os.environ.get('1rvN4OXg81SHDVoqENUmGy5KwAugH-48vuM2SikgE0l0')

# 金鑰檔案路徑（請輸入你的金鑰檔案路徑）
credential_file_path = 'credentials.json'

# auth_gsp_client 為我們建立來產生金鑰認證物件回傳給操作 Google Sheet 的客戶端 Client
def auth_gsp_client(file_path, scopes):
    # 從檔案讀取金鑰資料
    credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scopes)

    return gspread.authorize(credentials)

gsp_client = auth_gsp_client(credential_file_path, gsp_scopes)
# 我們透過 open_by_key 這個方法來開啟 sheet1 工作表一
worksheet = gsp_client.open_by_key(SPREAD_SHEETS_KEY).sheet1
# 每次清除之前資料
worksheet.clear()

# 將資料插入第 1 列
worksheet.insert_row(['測試資料欄 1', '測試資料欄 2'], 1)