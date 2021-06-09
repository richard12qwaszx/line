import os

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
    MessageEvent, TextMessage, TextSendMessage,
)
import pandas as pd

app = Flask(__name__)

# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN 類似聊天機器人的密碼，記得不要放到 repl.it 或是和他人分享。請替換成你的憑證內容
line_bot_api = LineBotApi('otPEz66uZklaipKpWyyKM7WvHu1fglGtzOa1ehbK0QakfJ8rk5JIquMfCrJeHx4KIBtGYSo10aAys3IiJIorTRirGghWF4jqOqPKvEXaLJ0HYOmm6KeUYRquGarz/h9+CablILpSoJnOXTJVm6H6iAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b64b328a82094718f2d68cc4f0c62b74')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('otPEz66uZklaipKpWyyKM7WvHu1fglGtzOa1ehbK0QakfJ8rk5JIquMfCrJeHx4KIBtGYSo10aAys3IiJIorTRirGghWF4jqOqPKvEXaLJ0HYOmm6KeUYRquGarz/h9+CablILpSoJnOXTJVm6H6iAdB04t89/1O/w1cDnyilFU=')
LINE_CHANNEL_SECRET = os.environ.get('b64b328a82094718f2d68cc4f0c62b74')

# 此為歡迎畫面處理函式，當網址後面是 / 時由它處理
@app.route("/", methods=['GET'])
def hello():
    return 'hello heroku'
 #此為 Webhook callback endpoint
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
    
    user_message = event.message.text
    reply_message = TextSendMessage(text='請輸入正確指令')
    stock_num = user_message
    df = pd.read_html(f'https://tw.stock.yahoo.com/q/q?s={stock_num}', encoding='big-5')
    df = pd.DataFrame(df[2])
    
    def crawl_for_stock_price():
        su=[]
        a=['股票代號', '時間', '成交','買進','賣出','漲跌','張數','昨收','開盤','最高','最低']

        for i in range(0,11):
            su.append(str(df.iloc[0][i]))
        serie = pd.Series( su, index=a)
        return serie
    a=crawl_for_stock_price()   
    reply_message = TextSendMessage(text=f'{a}')
    
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
    line_bot_api.reply_message(
        event.reply_token,
        reply_message)

# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__
if __name__ == "__main__":
    # 運行 Flask server
    app.run()