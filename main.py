import re, ffmpeg, io, openai, os
from google.cloud import speech

class Convert2audio:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def file_exists(self, dir, file):
        self.files = os.listdir(dir)
        if file in self.files:
            return True
        else:
            return False
        
    def convert(self):
        self.stream_input = ffmpeg.input(self.file_name)
        self.title = re.match(r'(.+?)\.\w+', self.file_name).group(1)
        self.audio_name = self.title + ".mp3"
        
        self.files = os.listdir(os.getcwd())

        if self.audio_name in self.files:
            return self.audio_name
        
        
        self.output = ffmpeg.output(self.stream_input, self.audio_name)
        ffmpeg.run(self.output)
        
        return self.audio_name
        

class Speech2text:
    def __init__(self, audio_name):
        self.audio_name = audio_name
        
    def convert(self):
        client = speech.SpeechClient()
        
        with io.open(self.audio_name, "rb") as f:
            self.content = f.read()
            
        self.audio = speech.RecognitionAudio(content=self.content)
        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            sample_rate_hertz=16000,
            language_code="ja-JP"
        )
        
        self.response = client.recognize(config=self.config, audio=self.audio)
        res = ""
        
        for result in self.response.results:
            #TODO: 結果をフロントに送信できるようにする
            res += result.alternatives[0].transcript+"\n"
            
        return res
        
class Chatgpt:
    def __init__(self, context):
        self.context = context
        
    def main(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.chat = []
        
        
        self.content = "あなたは就活生の面接における発言内容の校正を行います。特に敬語表現に気をつけながら括弧内の文章を校正し、\
            修正箇所を明示してください。敬語についてはこれらの記事を参考にしてください。\
                https://shinsotsu.mynavi-agent.jp/knowhow/article/learn-the-honorific.html\
                    また、修正箇所について解説もください。修正箇所等の報告については以下の形式でお願いします。\
                    【修正後の文章】\
                    「（ここに修正後の文章を挿入）」\
                    \
                    【解説】\
                    「（修正箇所の解説を挿入）」"
                    
        self.chat.append({"role": "system", "content": self.content})
        self.chat.append({"role": "user", "content": self.context})
        
        print("<ChatGPT>")
        
        self.response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",messages=self.chat
        )
        self.msg = self.response["choices"][0]["message"]["content"].lstrip()
        print(self.msg)
        self.chat.append({"role": "assistant", "content": self.msg})
        
            
            
#TODO: フロント側から動画タイトル受信            
movie_name = "test_movie.mp4"
audio_name = Convert2audio(movie_name).convert()
context = Speech2text(audio_name).convert()
Chatgpt(context).main()
