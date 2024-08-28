<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-sendpic

_✨ 基于图片api的发图插件，支持定时任务 ✨_



</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>



## 📖 介绍

本插件使用Anosu API获取图片，API网站：https://docs.anosu.top/

支持关键词搜索、定时发送图片到群里

## 💿 安装


<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-sendpic



## ⚙️ 配置
单纯发送功能无需额外配置

如需设置定时发送，请在 nonebot2 项目的`.env`文件中添加下表中的所有配置

|   配置项   | 必填 | 默认值 |      说明       |
| :-------: | :--: | :----: | :-------------: |
|  pic_num  |  否  |   无   |     发图数量     |
|  pic_tag  |  否  |   无   |    图片关键词    |
| pic_time  |  否  |   无   |     发图时间     |
| pic_group |  否  |   无   | 需要发送到的群号 |

其中，发图时间的配置请严格按照 `"x-hh-mm-ss"`的格式填写。

注：`x` 为定时模式，填"0"为每日定时发送，填"1"为按一定时间间隔发送

多个关键词请用 `|` 进行分隔

四个配置项均以列表形式填写，并 严格一一对应，例：
```
pic_num = [8,4,6]
pic_tag = ["御姐","","萝莉|金发"]
pic_time = ["0-18-00-00","0-08-00-00","1-00-00-30"]
pin_group = ["123456789","1145141919","123456789"]
```
上述配置表示
```
于每天 18:00:00 向群号"123456789"的群发送 8 张关键词为"御姐"的图
于每天 08:00:00 向群号"1145141919"的群发送 4 张无关键词的随机图
每隔 00:00:30（即30秒）向群号"123456789"的群发送 6 张关键词为"萝莉"、"金发"的图
```
## 🎉 使用
插件自带指令文档，发送 `发图帮助` 即可获取指令文档

发送 `发图` 即可获取随机图片，若bot有设置命令前缀，需加命令前缀，如 `/`

支持的参数：数量、关键词

使用方法： `发图 关键词 数量` ，多个关键词请用 `|` 进行分隔

不声明数量默认为1，不声明关键词则为随机发图

示例：
```
发图 原神 5
发图 碧蓝档案|爱丽丝 
发图 3
```
定时发送功能目前只能在bot端配置

## 可能遇到的问题
### 定时任务不执行
可能是apscheduler线程数满了，可以尝试在`.env`文件中添加
```
apscheduler_config={ "apscheduler. executors. processpool": {"type": "processpool","max_workers":"61"},"apscheduler. job_defaults. coalesce":"false","apscheduler. job_defaults:misfire_grace_time":"60","apscheduler. job_defaults. max_instances":"61" }
```

## 将来可能支持的功能
□支持使用指令直接设置定时任务

□接入更多图片api

□定时任务形式多样化

□...

## 还有些想说的
本仓库使用了nonebot-plugin-template的模板，谨向作者表示感谢

本人为普通大学生，并非计算机类的专业，水平有限，如有问题或建议请直接发issue，我会尽量解决
