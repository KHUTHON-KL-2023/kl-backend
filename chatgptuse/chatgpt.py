import openai

openai.api_key = "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"

text ="Do you want to go home?"

prompt0 = "다음 문장을 한국어로 해석해줘\n" + text
completion_trans = openai.chat.completions.create(
  model="gpt-4",
  temperature=0.2,
  messages=[
    {"role": "system", "content": "한국어 문법을 지켜야돼, 번역한 문장은 존대표현을 유지해줘"},
    {"role": "assistant", "content": "형식은 (번역한 문장)이야"},
    {"role": "user", "content": prompt0}
  ]
)

print(completion_trans.choices[0].message.content)
prompt1 = completion_trans.choices[0].message.content
#prompt1 = input("Q : ")
prompt1 = "다음 문장의 문법을 올바르게 수정해줘 만약, 올바른 문장이면 그대로 출력해줘\n" + prompt1

completion_gram = openai.chat.completions.create(
  model="gpt-4",
  temperature=0.2,
  messages=[
    {"role": "system", "content": "한국어 문법을 지켜야돼, 추가 설명은 필요 없어, 괄호 안에 문법이 올바른 문장"},
    {"role":"assistant","content":  "형식은 (문법을 수정한 문장)이야 만약, 올바른 문장이면 형식은 (문법이 올바른 문장)을 보내줘"},
    {"role": "user", "content": prompt1}
  ]
)

prompt2 = completion_gram.choices[0].message.content
print(prompt2)
prompt2 = "다음 문장을 격식체, 비격식체로 표현해줘\n" + prompt2

completion_up = openai.chat.completions.create(
    model="gpt-4",
    temperature=0.2,
    messages=[
    {"role": "system", "content": "한국어 문법을 지켜야돼. 입력한 문장이 평서문이면 평서문으로 알려주고 의문문이면 의문문, 명령문이면 명령문으로 알려줘."},
    {"role": "assistant", "content": " 형식은 (격식체: 받은 문장의 격식체, 비격식체: 받은 문장의 비격식체) 표의 형태로 알려줘"},
    {"role": "user", "content": prompt2}
  ]
)

print(completion_up.choices[0].message.content)
