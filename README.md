# 基于langchain的风水大师智能体(单Agents)
- version 1.0
- https://github.com/neilzhangpro
- AI学习笔记: https://1goto.ai
- [!English README](READEME_EN.md)
****


## 这是什么？
****
风水是中国传统文化中非常重要的组成部分，古人通过观察周围的万事万物，提出了朴素的世界观 —— 万事万物都有着千丝万缕的联系，天上的星辰映射着地面上的每一个人，你家里的物品摆放、朝向、甚至于你的姓名、出生日期都会对你的命运构成这样或那样的影响。
这个应用就是希望可以使用大语言模型，构建一个虚拟的风水先生，他可以与用户进行对话，帮助用户解答风水问题。而与传统的线上填写表单的机械式算命不同，我们希望构建一个有鲜明性格，能够尽量拟人的一个智能体。

## 主要特性
****
 - 基于Langchain构建的Agents：本应用非常适合新手学习AI Agents的构建
 - 完全可配置的任务性格：本应用默认以《鬼吹灯》中的陈瞎子为性格原型，你可以自行在Prompt中去构建自己想塑造的智能体
 - 基于Redis的长时记忆：使用Redis来做记忆存储，可实现不同用户的长时记录
 - 可扩展的工具能力：集成了在线搜索、本地RAG知识库、API访问三种工具能力，用户可以自行给Agent添加可使用的工具
 - 情感识别：可识别用户当前的输入情绪，并与输出联动
 - 动态音色的TTS合成：基于微软的mstts语言实现的动态音色合成
 - 无缝与Telegram bot结合
 - 支持同步输出和机遇websoket的流式输出，用户体验更好
 - 可扩展的知识库：内置从网页学习知识的RAG知识库，用户可以根据langchain文档，快速扩展其他支持的文档类型，实现chat2doc
 - 完全覆盖的测试用例，模块化代码配合单元测试，覆盖了大部分异常情况，为后期扩展打下基础。

 ## 为什么开发？
 ****
 - 事实上这个应用是我的在线网课《AI Agent智能应用从0到1定制开发》https://coding.imooc.com/class/822.html 的实战代码，然而由于之前课程开发时间紧张，代码比较的丑陋，于是抽时间对其进行了重构。

 - 智能体的开发，尤其是基于Langchain的开发比较难上手，学习曲线比较陡峭，所以有一套这样的模板，也非常适合在不同的项目里作为项目起始模板，如果你觉得对你有用的话，麻烦给个start。

 ## 如何使用？
 ****
 - 推荐开发环境：windows+vscode+python3.12
 - git clone 本仓库
 - 由于3.12自带venv，所以我们直接创建虚拟环境
```bash
python -m venv FengShuiAgents
```
- 在windows上激活虚拟环境
```bash
FengShuiAgents\Scripts\activate
```
- 在 macOS 和 Linux 上
```bash
source FengShuiAgents/bin/activate
```
- 激活后，你会看到命令行提示符前面出现 (FengShuiAgents)。
- 安装项目依赖包
```bash
pip install -r requirements.txt
```
- 安装完毕后，可以直接运行
- 在根目录创建.env配置文件，配置类似大模型key以及其他资源的key
```bash
OPENAI_API_KEY=""
OPENAI_API_BASE=""
AZURE_API_KEY=""
USER_AGENT="FengShuiAgents/1.0"
SERPAPI_API_KEY= ""
API_KEY = ""
Telegram_API_KEY = ""
```
- 运行Server端:
```bash
python -m src.Server
```
- 在src/Client/Telegram.py中设置你的Telegram bot的key
- 运行客户端:
```bash
python .\src\Client\Telegram.py
```
- 本机安装redis并打开redis server
- 打开你配置好的Telegram bot可以开始对话了
- 打开接口文档： http://localhost:8000/docs
- 同步输出接口为：http://localhost:8000/chat
- 流式输出接口为: ws://localhost:8000/ws
- RAG入库接口为（网页内容）: http://localohost:8000/add_urls

## 依赖资源
- OPENAI的KEY或国产大模型的API KEY
- 微软云的TTS资源和API
- 命理网站API权限
- SerpAPI的API KEY

## 其他
- Tools中仅仅写了三个示例，这里留给拥有无限想象力的你去自由扩展
- 这是一个典型的单Agents，后期会更新两个基于Langgraph和CrewAI的多Agents版本
- 对于Python用的不爽的同学，typescript也在路上
- 欢迎多提问题，如果有帮助到你，也请给仓库打个Start!
