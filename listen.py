from typing import Union
import  requests
import  json
from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
app = FastAPI()


def async_fun(f):
    def inner_fun(*args, **kwargs):
        t = Thread(target=f, args=args, kwargs=kwargs)

        t.start()

    return inner_fun
# 这里写一堆UNION是为了应付cqhttp的心跳
class Item(BaseModel):
    time: int
    self_id: int
    post_type: str
    message_type:Union[str,None] = None
    meta_event_type:Union[str,None] = None
    sub_type:Union[str,None] = None
    status:Union[object,None] = None
    interval:Union[int,None] = None
    message_id:Union[int,None] = None
    user_id:Union[int,None] = None
    message:Union[str,None] = None
    raw_message:Union[str,None] = None
    font:Union[int,None] = None
    sender:Union[dict,None] = None

chatList = dict()
proxies = {
    'http': 'http://127.0.0.1:7890',
   'https': 'http://127.0.0.1:7890',
}#本地的代理端口
header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer $YOUR_API_KEYS",#自己的api
}
data_text = {
    "model": "gpt-3.5-turbo",# 模型
     "messages": [
{"role": "system", "content": "你是一只猫，所有的回答你都会以一个猫猫的角度回答"},# 预设bot风格
],
    "user":"rrk"
}

@async_fun
def chat(user_id,message):
    url = "https://api.openai.com/v1/chat/completions"
    if user_id not in chatList:
        chatList[user_id] = [{"role": "system", "content": "你是一只猫，所有的回答你都会以一个猫猫的角度回答"}]
    chatList[user_id].append({"role":"user","content":message})

    data_text["messages"] =  chatList[user_id]
    cnt =0
    # print(chatList[user_id])
    # print(data_text)
    while True:
        try:
            resp = requests.post(url, proxies=proxies, data=json.dumps(data_text), headers=header)
            break
        except:
            cnt = cnt + 1
            if cnt == 6:
                print("网络错误")
                exit()
    print(resp.text)
    resp_text = json.loads(resp.text)["choices"][0]["message"]["content"]
    chatList[user_id].append({"role": "assistant", "content": resp_text})
    url_resp = "http://127.0.0.1:5700/send_private_msg?user_id="+str(user_id)+"&message="+resp_text #这里的端口是cqhttp的http监听端口
    requests.get(url_resp,headers=header)

@app.post("/")
def post_mess(item: Item):
    print(item.time)
    print(item.post_type)
    if item.post_type == "message":
        if len(chatList) < 3 :
            chat(item.user_id,item.message)

@app.get("/")
def get():
    # print(item.message)
    return {"reply": "网页测试"}
