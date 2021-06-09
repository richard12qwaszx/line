
# 引入套件 flask
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
# 引入 linebot 異常處理
from linebot.exceptions import (
    InvalidSignatureError
)
# 引入 linebot 訊息元件
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage)
import gspread
import pandas as pd
import json
#from oauth2client.service_account import ServiceAccountCredentials 
import requests
import os
import time
app = Flask(__name__)

# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN 類似聊天機器人的密碼，記得不要放到 repl.it 或是和他人分享
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
#credential_file_path = 'credentials.json'
#gsp_scopes = ['https://spreadsheets.google.com/feeds']
#SPREAD_SHEETS_KEY = os.environ.get('SPREAD_SHEETS_KEY')#1t_Fpsk4W-twpiosSjndde_P3StOQMJ-g-xeAe6oj8kE
def crawl_for_stock_price(stock_num):
        su=[]
        a=['股票代號', '時間', '成交','買進','賣出','漲跌','張數','昨收','開盤','最高','最低']
        df = pd.read_html(f'https://tw.stock.yahoo.com/q/q?s={stock_num}', encoding='big-5')
        df = pd.DataFrame(df[2])

        for i in range(0,11):
            su.append(str(df.iloc[0][i]))
        serie = pd.Series( su, index=a)
        return serie
def Stock_health_check(stock_num):
    st_list=['股　性', '除權除息日', '經營力','配息(元/股)','獲利力','資配(股/張)','成長力','盈配(股/張)','償債力','現增配(股/張)','近1年殖利率','5日(週)均線','近3年殖利率','20日(月)均線','近5年殖利率','60日(季)均線']
    fun=[]
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'} 
    url=f'https://news.money-link.com.tw/yahoo/0061_{stock_num}.html'
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    df = pd.read_html(resp.text)
    df = pd.DataFrame(df[0])
    #健檢
    #1
    sf1=df.iloc[0][0].split('：',1)
    fun.append(sf1[1])
    #2
    fun.append(df.iloc[0][3])
    #3
    sf2=df.iloc[1][0].split('：',1)
    fun.append(sf2[1])
    #4
    fun.append(df.iloc[1][3])
    #5
    sf3=df.iloc[2][0].split('：',1)
    fun.append(sf3[1])
    #6
    fun.append(df.iloc[2][3])
    #7
    sf4=df.iloc[3][0].split('：',1)
    fun.append(sf4[1])
    #8
    fun.append(df.iloc[3][3])
    #9
    sf5=df.iloc[4][0].split('：',1)
    fun.append(sf5[1])
    #10
    fun.append(df.iloc[4][3])
    #11
    fun.append(df.iloc[5][1])
    #12
    fun.append(df.iloc[5][3])
    #13
    fun.append(df.iloc[6][1])
    #14
    fun.append(df.iloc[6][3])
    #15
    fun.append(df.iloc[7][1])
    #16
    fun.append(df.iloc[7][3])
    serie2 = pd.Series( fun, index=st_list)
    return serie2

#def auth_gsp_client(file_path, scopes):
    # 從檔案讀取金鑰資料
#    credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scopes)

 #   return gspread.authorize(credentials)


#gsp_client = auth_gsp_client(credential_file_path, gsp_scopes)
# 我們透過 open_by_key 這個方法來開啟工作表一 worksheet
#worksheet = gsp_client.open_by_key(SPREAD_SHEETS_KEY).sheet1



# 此為 Webhook callback endpoint
@app.route("/", methods=['GET'])
def hello():
    return 'hello heroku'
@app.route("/callback", methods=['POST'])
def callback():
    # 取得網路請求的標頭 X-Line-Signature 內容，確認請求是從 LINE Server 送來的
    signature = request.headers['X-Line-Signature']

    # 將請求內容取出
    body = request.get_data(as_text=True)

    # handle webhook body（轉送給負責處理的 handler，ex. handle_message）
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #讀取朋友line資訊
    user_message = str(event.message.text).upper().split(':',1)
    thing=user_message[0]
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    #display_name = profile.display_name
    uid = profile.user_id
    if thing == '即時股價':    
        a=crawl_for_stock_price(user_message[1])   
        reply_message = TextSendMessage(text=f'{a}')
        line_bot_api.push_message(uid, reply_message)
    elif thing == '股票健診':
        doing=Stock_health_check(user_message[1])
        reply_message = TextSendMessage(text=f'{doing}')
        line_bot_api.push_message(uid, reply_message)

    # 回傳訊息給使用者
    #line_bot_api.reply_message(event.reply_token,reply_message)
    

# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__
if __name__ == "__main__":
    # 運行 Flask server，預設設定監聽 127.0.0.1 port 5000（網路 IP 位置搭配 Port 可以辨識出要把網路請求送到那邊 xxx.xxx.xxx.xxx:port，app.run 參數可以自己設定監聽 ip/port）
    app.run()

#reply_message= TextSendMessage(text=f'你好{display_name}!')
    #line_bot_api.reply_message(event.reply_token,reply_message)
    #times=time . strftime (  '%Y/%m/%d'   , time . localtime ( ) )
    #values_list = worksheet.col_values(1)
    #reply_message = TextSendMessage(text=f'{thing}')
    #if user_id in values_list:
    # 回傳 user_id 在 list 中所在 index
    #    index = values_list.index(user_id)
        # 新增到同一個 User Id 位置的日期欄位
    #    worksheet.update(f'B{index+1}', f'{times}')
    #else:
    #    worksheet.append_row([user_id, times, display_name])