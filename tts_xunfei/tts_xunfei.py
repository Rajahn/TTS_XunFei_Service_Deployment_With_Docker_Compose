import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

global tts_in_progress
tts_in_progress = False


class Ws_Param:
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "lame", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8", "sfl": 1,
                             "speed": 80}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            with open('./output.mp3', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### 链接关闭 ###")


def on_open(ws, ifly):
    def run(*args):
        d = {"common": ifly.CommonArgs,
             "business": ifly.BusinessArgs,
             "data": ifly.Data,
             }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists('./output.mp3'):
            os.remove('./output.mp3')

    thread.start_new_thread(run, ())


def generate_audio(text):
    ifly = Ws_Param(APPID='dec60e28', APISecret='MzMzMGFkYjI2MzAyMjk2MjUzMTRhOTRl',
                    APIKey='b492175e9919700929dca6b5e0f7dace',
                    Text=text)
    websocket.enableTrace(False)
    wsUrl = ifly.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_close=on_close)
    ws.on_open = lambda ws: on_open(ws, ifly)  # 使用lambda传入ifly
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


@app.route('/tts', methods=['POST'])
def tts_api():
    global tts_in_progress

    if tts_in_progress:  # 如果tts已经在运行，返回一个错误消息
        return jsonify({"error": "TTS is already in progress, please wait!"}), 429

    data = request.get_json()
    text = data.get('text')[0]
    print(text)
    if not text:
        return jsonify({"error": "Text is required!"}), 400

    tts_in_progress = True  # 设置标志为True，表示tts正在执行
    # time.sleep(30)
    generate_audio(text)
    tts_in_progress = False  # 重置标志为False，表示tts已经完成

    try:
        with open('output.mp3', 'rb') as f:
            audio_data = f.read()
            return audio_data
    except Exception as e:
        return jsonify({"error": f"Failed to read the audio file! Error: {str(e)}"}), 500

@app.route('/check_tts_status', methods=['GET'])
def check_tts_status():
    global tts_in_progress
    return jsonify({"status": not tts_in_progress})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

