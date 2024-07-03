from telethon import TelegramClient, sync
import os
from vendor.class_bot import LYClass  # 导入 LYClass
import asyncio
import time

# 检查是否在本地开发环境中运行
if not os.getenv('GITHUB_ACTIONS'):
    from dotenv import load_dotenv
    load_dotenv()

# 从环境变量中获取值
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
session_name = api_id+'session_name'  # 确保与上传的会话文件名匹配

# 创建客户端
client = TelegramClient(session_name, api_id, api_hash)

# 创建 LYClass 实例
ly_class_instance = LYClass('text')

# 定义消息处理函数
async def process_message(message):
    try:
        await asyncio.sleep(3)
        # print(f"Processing message: {message}\n")
        print(f"Processing message: {message.id}\n")
        if message.reply_to:
            print(f"Message has reply_to: {message.reply_to.reply_to_msg_id}\n")

        message_handlers = {
            50074: ly_class_instance.datapan,
            43058: ly_class_instance.mediabk,
            43064: ly_class_instance.showfiles,
            43060: ly_class_instance.blgg,
            43062: ly_class_instance.filesave,
            43072: ly_class_instance.wangpan,
            43066: ly_class_instance.filetobot,
            43070: ly_class_instance.fileoffrm,
            43068: ly_class_instance.filein
        }

        reply_id = message.reply_to.reply_to_msg_id if message.reply_to else None
        handler = message_handlers.get(reply_id)

        if handler:
            if asyncio.iscoroutinefunction(handler):
                await handler(client, message)
            else:
                handler(message)
        else:
            print(f"Unhandled thread ID: {message.reply_to.reply_to_msg_id if message.reply_to else 'None'} - Message: {message.sender_id}, {message.text}\n")
    except Exception as e:
        print(f"An error occurred while processing message: {e}\n")

async def main():
    await client.start(phone_number)

    # 使用指定的 chat_id
    chat_id = -1001717350482

    start_time = time.time()
    while True:
        # 获取最近5条消息
        async for message in client.iter_messages(chat_id, limit=5):
            if message.reply_to:
                await process_message(message)
        
        # 检查累计执行时间是否超过5分钟
        elapsed_time = time.time() - start_time
        if elapsed_time > 280:  # 300秒等于5分钟
            print("Execution time exceeded 5 minutes. Stopping.")
            break
        else:
            print("Execution time is "+str(elapsed_time)+" seconds. Continuing...")
        
        await asyncio.sleep(15)  # 间隔15秒

    
            

with client:
    client.loop.run_until_complete(main())
