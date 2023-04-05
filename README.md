# CHAT_BOT_FASTAPI
## 使用方式
```shell
uvicorn listen:app --reload
#如果需要预设端口可以自己百度
#需要配合GO_CQHTTP使用,yml文件根据代码中的端口进行相应的更改
#代码中没有使用openai提供的api，可以自己设置proxy参数
```
只实现了私聊窗口的基于服务器运行时间的聊天记录chat回复
