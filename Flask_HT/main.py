from flask import Flask, jsonify, Response
from functools import wraps
import openai
import speech_recognition as sr
import pyaudio
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

openai.api_key = "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"

def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

@app.route('/')
@as_json
def home():
    return "hello world!"

@app.route('/json')
@as_json
def data():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speack Anything :')
        audio = r.listen(source)
        
        try:
            sound_to_text = r.recognize_google(audio)
            print('You said : {}'.format(sound_to_text))
        except:
            print('Sirry could not recignize your voice')

    #sound_to_text = "hello world"  

    trans_text = "다음 문장을 한국어로 해석해줘\n" + sound_to_text
    completion_trans = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "한국어 문법을 지켜야돼, 번역한 문장은 존대표현을 유지해줘"},
        {"role": "assistant", "content": "형식은 (번역한 문장)이야"},
        {"role": "user", "content": trans_text}
    ]
    )

    gram_text = completion_trans.choices[0].message.content
    up_text = "다음 문장의 문법을 올바르게 수정해줘\n" + gram_text

    completion_gram = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "한국어 문법을 지켜야돼, 추가 설명은 필요 없어, 괄호 안에 문법이 올바른 문장"},
        {"role":"assistant","content":  "형식은 (문법을 수정한 문장)이야 만약, 올바른 문장이면 형식은 (문법이 올바른 문장)을 보내줘"},
        {"role": "user", "content": gram_text}
    ]
    )

    up_text = completion_gram.choices[0].message.content
    save_text = up_text
    up_text = "다음 문장을 격식체, 비격식체로 표현해줘\n" + up_text

    completion_up = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "한국어 문법을 지켜야돼. 입력한 문장이 평서문이면 평서문으로 알려주고 의문문이면 의문문, 명령문이면 명령문으로 알려줘"},
        {"role": "assistant", "content": " 형식은 (격식체: 받은 문장의 격식체, 비격식체: 받은 문장의 비격식체) 표의 형태로 알려줘"},
        {"role": "user", "content": up_text}
    ]
    )

    #print(completion_up.choices[0].message.content)
    cutting_index = completion_up.choices[0].message.content.find("비격식체")
    upper = completion_up.choices[0].message.content[:cutting_index]
    lower = completion_up.choices[0].message.content[cutting_index:]

    from konlpy.tag import Okt
    okt = Okt()
    result = okt.nouns(save_text)

    return{
        "origin" : sound_to_text, "trans" : save_text, "up" : upper, "down" : lower
    }

@app.route('/input/<string:sentence>')
@as_json
def jsonData():
    sound_to_text = sentence

    trans_text = "다음 문장을 한국어로 해석해줘\n" + sound_to_text
    completion_trans = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "한국어 문법을 지켜야돼, 번역한 문장은 존대표현을 유지해줘"},
        {"role": "assistant", "content": "형식은 (번역한 문장)이야"},
        {"role": "user", "content": trans_text}
    ]
    )

    gram_text = completion_trans.choices[0].message.content
    up_text = "다음 문장의 문법을 올바르게 수정해줘\n" + gram_text

    completion_gram = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "한국어 문법을 지켜야돼, 추가 설명은 필요 없어, 괄호 안에 문법이 올바른 문장"},
        {"role":"assistant","content":  "형식은 (문법을 수정한 문장)이야 만약, 올바른 문장이면 형식은 (문법이 올바른 문장)을 보내줘"},
        {"role": "user", "content": gram_text}
    ]
    )

    up_text = completion_gram.choices[0].message.content
    save_text = up_text
    up_text = "다음 문장을 격식체, 비격식체로 표현해줘\n" + up_text

    completion_up = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "한국어 문법을 지켜야돼. 입력한 문장이 평서문이면 평서문으로 알려주고 의문문이면 의문문, 명령문이면 명령문으로 알려줘"},
        {"role": "assistant", "content": " 형식은 (격식체: 받은 문장의 격식체, 비격식체: 받은 문장의 비격식체) 표의 형태로 알려줘"},
        {"role": "user", "content": up_text}
    ]
    )

    #print(completion_up.choices[0].message.content)
    cutting_index = completion_up.choices[0].message.content.find("비격식체")
    upper = completion_up.choices[0].message.content[:cutting_index]
    lower = completion_up.choices[0].message.content[cutting_index:]

    from konlpy.tag import Okt
    okt = Okt()
    result = okt.nouns(save_text)

    return{
        "origin" : sound_to_text, "trans" : save_text, "up" : upper, "down" : lower
    }

if __name__ == '__main__':
    app.run(debug=True)