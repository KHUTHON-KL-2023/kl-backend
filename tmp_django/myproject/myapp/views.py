from django.shortcuts import render
from django.http import JsonResponse
import openai
import speech_recognition as sr
import pyaudio

openai.api_key = "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"

def process_speech(request):
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speack Anything :')
        audio = r.listen(source)
        
        try:
            sound_to_text = r.recognize_google(audio)
            print('You said : {}'.format(sound_to_text))
        except:
            print('Sirry could not recignize your voice')
    """
    sound_to_text = "Hello. My name is John."

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

    cutting_index = completion_up.choices[0].message.content.find("비격식체")
    upper = completion_up.choices[0].message.content[:cutting_index]
    lower = completion_up.choices[0].message.content[cutting_index:]

    from konlpy.tag import Okt
    okt = Okt()
    result_noun = okt.nouns(save_text)

    return JsonResponse({'trans' : save_text, 'up' : upper, "low" : lower, "nouns" : result_noun })
