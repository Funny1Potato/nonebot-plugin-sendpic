from nonebot import get_plugin_config, get_bot
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from .config import Config
import json
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import os
from pathlib import Path

__plugin_meta__ = PluginMetadata(
    name="无情的发图姬",
    description="基于图片api的发图插件，支持定时任务",
    usage="发送 发图帮助 即可获取指令文档",
    config=Config,
    type="application",
    homepage="https://github.com/Funny1Potato/nonebot-plugin-sendpic",
    supported_adapters={"~onebot.v11"},
)


config = get_plugin_config(Config)
from nonebot import on_notice, on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    Message,
    GroupMessageEvent,
    ActionFailed,
)
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

from httpx import AsyncClient


async def get_pic(num:int,tag:str):
    async with AsyncClient() as session:
        url ='https://image.anosu.top/pixiv/json'  #图片url
        params = {'num':num,'keyword':tag}  #获取参数
        pic = await session.get(url,params = params)  #请求数据 
        list1 = json.loads("".join(x for x in pic.text if x.isprintable()))  #结果处理
        logger.success("已获取图片")
        return [x["url"] for x in list1]  #上报url

async def get_pic_max(num:int,tag:str):
    async with AsyncClient() as session:
        tt = config.pic_correct
        url ='https://image.anosu.top/pixiv/json'  #图片url
        params = {'num':num,'keyword':tag}  #获取参数
        pic = await session.get(url,params = params)  #请求数据 
        list1 = json.loads("".join(x for x in pic.text if x.isprintable()))  #结果处理
        p = []
        for x in list1:
            p.append(x["url"])
        t = 0
        while len(p) < num:
            nn = num - len(p)
            url ='https://image.anosu.top/pixiv/json'  #图片url
            params = {'num':nn,'keyword':tag}  #获取参数
            pic = await session.get(url,params = params)  #请求数据 
            list1 = json.loads("".join(x for x in pic.text if x.isprintable()))
            for x in list1:
                p.append(x["url"])
            t = t + 1
            if t == tt:
                break
        logger.success("已获取图片")
        return p  #上报url


#自动任务函数部分   
async def pic(**setting):
    bot: Bot = get_bot()
    k = setting["i"]  #读取计时器传递的信息
    #读取并处理配置
    num1 = config.pic_num
    tag1 = config.pic_tag
    group1 = config.pic_group
    num = num1[k]
    tag = tag1[k]
    group = group1[k]
    num = int(num)  

    p = await get_pic(num,tag)  #获取图片
    for i in range(num):
        url = p[i]  #逐个提取列表中的图片url
        group_id = int(group)
        try:
            await bot.send_group_msg(group_id=group_id, message=MessageSegment.image(url))  #发送到列表中的群
        except:
            continue

#自动任务计时部分
try:
    a = config.pic_num
    b = config.pic_tag
    c = config.pic_time
    d = config.pic_group
    if len(a)==len(b)==len(c)==len(d):  #检测配置是否有一一对应
        l = len(c)
        for i in range(l):  
            cc = c[i]
            c1,c2,c3,c4 = cc.split("-")
            c1 = int(c1)
            c2 = int(c2)
            c3 = int(c3)
            c4 = int(c4)  #读取并处理时间配置
            if c1 == 0:
                scheduler.add_job(pic, 'cron', hour=c2, minute=c3, second=c4, kwargs={"i":i})  #定时
            else:
                scheduler.add_job(pic, 'interval', hours=c2, minutes=c3, seconds=c4, kwargs={"i":i})  #时间间隔
    else:
        logger.error("自动发图功能配置错误，请检查")
except:
    logger.error("自动发图功能未配置")



#发图指令部分
pixiv = on_command("发图")

@pixiv.handle()
async def pix(args: Message = CommandArg()):
    tt = config.pic_correct
    if tt != 0:
        pixiv.skip()
    if data := args.extract_plain_text():
        try:
            tag,num = data.split()  #提取输入的数字和tag
        except:
            try:
                num = int(data)
                tag = ""  #只填数量没填tag，tag为空
            except:
                tag = data
                num = 1  #未填数量，默认为1
        j = 0
        try:
            try:
                num = int(num)
            except:
                temp = num
                num = tag
                tag = temp  #尝试修正错误的参数顺序
                try:
                    num = int(num)  
                except:
                    await pixiv.finish("参数错误，请检查输入是否正确")
            p = await get_pic(num,tag)  #获取图片
            if len(p) == 0:
                await pixiv.finish("搜索失败，可能是网络问题或是输入的关键词搜不到图")
            await pixiv.send("正在努力发送中，受网络影响可能实际发出的图片数较少")
            for i in range(num):
                url = p[i]  #逐个提取图片url
                try:
                    await pixiv.send(MessageSegment.image(url))
                except:
                    j = j + 1
                    continue
            logger.success(f"已发送{num - j}张图，{j}张图发送失败")
            if j == num:
                await pixiv.finish("发送失败了，请重试")
            else:
                await pixiv.finish(f"发送完成，已发送{num - j}张图")
        except:
            return
    else:
        tag = ""  #tag不填则为空
        num = 1  #数量默认为1
        j = 0
        try:
            num = int(num)
            p = await get_pic(num,tag)  #获取图片
            if len(p) == 0:
                await pixiv.finish("找图失败，可能是网络问题导致搜不到图")
            await pixiv.send("正在努力发送中，请稍等")
            url = p[0]  #提取图片url
            try:
                await pixiv.send(MessageSegment.image(url))
            except:
                j = j + 1
            logger.success(f"已发送{num - j}张图，{j}张图发送失败")
            if j == num:
                await pixiv.finish("发送失败了，请重试")
            else:
                await pixiv.finish(f"发送完成，已发送{num - j}张图")
        except:
            return
        
@pixiv.handle()
async def pix_max(args: Message = CommandArg()):
    tt = config.pic_correct
    if tt == 0:
        pixiv.skip()
    if data := args.extract_plain_text():
        try:
            tag,num = data.split()  #提取输入的数字和tag
        except:
            try:
                num = int(data)
                tag = ""  #只填数量没填tag，tag为空
            except:
                tag = data
                num = 1  #未填数量，默认为1
        j = 0
        try:
            try:
                num = int(num)
            except:
                temp = num
                num = tag
                tag = temp  #尝试修正错误的参数顺序
                try:
                    num = int(num)  
                except:
                    await pixiv.finish("参数错误，请检查输入是否正确")
            p = await get_pic_max(num,tag)  #获取图片
            if len(p) == 0:
                await pixiv.finish("搜索失败，可能是网络问题或是输入的关键词搜不到图")
            await pixiv.send("正在努力发送中...")
            for i in range(num):
                url = p[i]  #逐个提取图片url
                try:
                    await pixiv.send(MessageSegment.image(url))
                except:
                    j = j + 1
                    continue
            k = num - j
            t = 0
            while k < num:
                nn = num - k
                p = await get_pic_max(nn,tag)  #获取图片
                for i in range(nn):
                    url = p[i]  #逐个提取图片url
                    try:
                        await pixiv.send(MessageSegment.image(url))
                        k = k + 1
                    except:
                        continue
                t = t + 1
                if t == tt:
                    break
            logger.success(f"已发送{k}张图，{num - k}张图发送失败")
            if k == 0:
                await pixiv.finish("发送失败了，请重试")
            else:
                await pixiv.finish(f"发送完成，已发送{k}张图")
        except:
            return
    else:
        tag = ""  #tag不填则为空
        num = 1  #数量默认为1
        j = 0
        try:
            num = int(num)
            p = await get_pic_max(num,tag)  #获取图片
            if len(p) == 0:
                await pixiv.finish("找图失败，可能是网络问题导致搜不到图")
            await pixiv.send("正在努力发送中...")
            url = p[0]  #提取图片url
            try:
                await pixiv.send(MessageSegment.image(url))
            except:
                j = j + 1
            k = num - j
            t = 0
            while k < num:
                nn = num - k
                p = await get_pic_max(nn,tag)  #获取图片
                url = p[0]  #提取图片url
                try:
                    await pixiv.send(MessageSegment.image(url))
                    k = k + 1
                except:
                    continue
                t = t + 1
                if t == tt:
                    break
            logger.success(f"已发送{k}张图，{num - k}张图发送失败")
            if k == 0:
                await pixiv.finish("发送失败了，请重试")
            else:
                await pixiv.finish(f"发送完成，已发送{k}张图")
        except:
            return

#自带插件文档
botdoc = on_command("发图帮助")

@botdoc.handle()
async def phelp():
    if not os.path.exists("./data/sendpic/help.png"):
        try:
            os.mkdir("./data")
        except:
            try:
                os.mkdir("./data/sendpic")   # 创建文件夹
            except:
                pass   
        async with AsyncClient() as session:
            response = await session.get("https://link.funnypotato.cn/sendpic.png")
            open("./data/sendpic/help.png", "wb").write(response.content)  #下载文件
    url = Path("./data/sendpic/help.png")
    await botdoc.finish(MessageSegment.image(url))


    

