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
import requests
import pandas as pd

app = Flask(__name__)

# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN 類似聊天機器人的密碼，記得不要放到 repl.it 或是和他人分享
line_bot_api = LineBotApi('1ZtuxzKLdlLvufiBo82hbGli+LuHAnXPMbhZLkSMIzlg2HJOyI4vw0Eag/zWayI8ygZ/ryur6znHgvoMFicIjrzMeyrQM/Cum3fytvQdmJyusPG9a2Pat7Nl30ZMR4mSYgqd1bV/LPPce6aomJ5ISwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ae047099c2056bf696abb23fb3859f66')
#line_bot_api = os.environ.get('1ZtuxzKLdlLvufiBo82hbGli+LuHAnXPMbhZLkSMIzlg2HJOyI4vw0Eag/zWayI8ygZ/ryur6znHgvoMFicIjrzMeyrQM/Cum3fytvQdmJyusPG9a2Pat7Nl30ZMR4mSYgqd1bV/LPPce6aomJ5ISwdB04t89/1O/w1cDnyilFU=')
#handler = os.environ.get('ae047099c2056bf696abb23fb3859f66')
new=['股票代號','時間','成交','買進','賣出','漲跌','張數','昨收','開盤','最高','最低']

now=[]



# 此為 Webhook callback endpoint
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
    #reply_message = TextSendMessage(text='請輸入正確指令')
    # 根據使用者輸入 event.message.text 條件判斷要回應哪一種訊息
    df = pd.read_html(f'https://tw.stock.yahoo.com/q/q?s={user_message}', encoding='big-5')
    df = pd.DataFrame(df[2])
    for i in range(0,11):
        df1=now.append(df.iloc[0][i])
    for u in range(0,11):
        print(new[u])
        reply_message = TextSendMessage(text=f'{now(u)}')
    
    




    line_bot_api.reply_message(
        event.reply_token,
        reply_message)
# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__
if __name__ == "__main__":
    # 運行 Flask server，預設設定監聽 port 5000（網路 IP 位置搭配 Port 可以辨識出要把網路請求送到那邊 xxx.xxx.xxx.xxx:port）
    app.run()