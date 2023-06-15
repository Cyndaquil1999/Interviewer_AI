import json
from urllib import request
import speech_recognition as sr

APPID = "Yout Client ID"  # <-- ここにあなたのClient ID（アプリケーションID）を設定してください。
URL = "https://jlp.yahooapis.jp/KouseiService/V2/kousei"
listener = sr.Recognizer()

def post(query):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Yahoo AppID: {}".format(APPID),
    }
    param_dic = {
      "id": "1234-1",
      "jsonrpc" : "2.0",
      "method": "jlp.kouseiservice.kousei",
      "params" : {
         "q": query
      }
    }
    params = json.dumps(param_dic).encode()
    req = request.Request(URL, params, headers)
    with request.urlopen(req) as res:
        body = res.read()
    return body.decode()


try:
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        voice_text = listener.recognize_google(voice, language="ja-JP")
        print(voice_text)

        #json.loads()でstr->JSON
        response = json.loads(post(voice_text))

        for dic in response["result"]["suggestions"]:
            note = dic["note"]
            rule = dic["rule"]
            suggestion = dic["suggestion"]
            word = dic["word"]
            print(f"検出された文字: {word} \n提案された表現: {suggestion} \n理由: {rule} \n備考: {note} \n")

        

except:
    print('sorry I could not listen')
