# Feng Shui Master Agent Based on Langchain (Single Agents)
- version 1.0
- https://github.com/neilzhangpro
- AI Learning Notes: https://1goto.ai
****
## What is this?
****
Feng Shui is a very important part of Chinese traditional culture. The ancients proposed a simple worldview by observing everything around them - everything is inextricably linked, the stars in the sky reflect everyone on the ground, the placement and orientation of items in your home, and even your name and date of birth will have one or another impact on your destiny.
This application hopes to use a large language model to build a virtual Feng Shui master who can talk to users and help users answer Feng Shui questions. Unlike the traditional mechanical fortune-telling that fills out forms online, we hope to build an agent with a distinct personality and can be as anthropomorphic as possible.

## Main features
****
- Agents built on Langchain: This application is very suitable for beginners to learn how to build AI Agents
- Fully configurable task personality: This application uses Chen Xiazi in "Ghost Blowing Light" as the character prototype by default. You can build the intelligent body you want to shape in Prompt
- Long-term memory based on Redis: Using Redis for memory storage can achieve long-term records of different users
- Extensible tool capabilities: Integrates three tool capabilities: online search, local RAG knowledge base, and API access. Users can add available tools to Agents by themselves
- Emotion recognition: Can recognize the user's current input emotions and link them with output
- TTS synthesis of dynamic timbre: Dynamic timbre synthesis based on Microsoft's mstts language
- Seamless integration with Telegram bot
- Supports synchronous output and streaming output of opportunity websoket, with better user experience
- Extensible knowledge base: Built-in RAG knowledge base for learning knowledge from web pages. Users can quickly expand other supported document types based on langchain documents to achieve chat2doc
- Fully covered test cases, modular code with unit testing, covering most of the abnormal situations, laying the foundation for later expansion.

## Why develop?
****
- In fact, this application is the actual code of my online course "AI Agent Intelligent Application Custom Development from 0 to 1" https://coding.imooc.com/class/822.html. However, due to the tight development time of the previous course, the code is relatively ugly, so I took the time to refactor it.

- The development of intelligent agents, especially the development based on Langchain, is difficult to get started, and the learning curve is relatively steep, so there is a set of such templates, which is also very suitable as a project starting template in different projects. If you think it is useful to you, please give it a start.

## How to use it?
****
- Recommended development environment: windows+vscode+python3.12
- git clone this repository
- Since 3.12 comes with venv, we directly create a virtual environment
```bash
python -m venv FengShuiAgents
```
- Activate the virtual environment on windows
```bash
FengShuiAgents\Scripts\activate
```
- On macOS and Linux
```bash
source FengShuiAgents/bin/activate
```
- After activation, you will see (FengShuiAgents) appear in front of the command line prompt.
- Install project dependencies
```bash
pip install -r requirements.txt
```
- After installation, you can run it directly
- Create a .env configuration file in the root directory and configure keys such as large model keys and other resources
```bash
OPENAI_API_KEY=""
OPENAI_API_BASE=""
AZURE_API_KEY=""
USER_AGENT="FengShuiAgents/1.0"
SERPAPI_API_KEY= ""
API_KEY = ""
Telegram_API_KEY = ""
```
- Run the server:
```bash
python -m src.Server
```
- Set the key of your Telegram bot in src/Client/Telegram.py
- Run the client:
```bash
python .\src\Client\Telegram.py
```
- Install redis on your local machine and open the redis server
- Open your configured Telegram bot to start a conversation
- Open the interface document: http://localhost:8000/docs
- Synchronous output interface: http://localhost:8000/chat
- Streaming output interface: ws://localhost:8000/ws
- RAG storage interface (webpage content): http://localohost:8000/add_urls

## Dependent resources
- OPENAI KEY or domestic large model API KEY
- Microsoft Cloud TTS resources and API
- Numerology website API permissions
- SerpAPI API KEY

## Others
- Only three examples are written in Tools, which are left for you to expand freely with unlimited imagination
- This is a typical single agent, and two multi-agent versions based on Langgraph and CrewAI will be updated later
- For students who are not comfortable with Python, typescript is also on the way
- Welcome to ask more questions, if it helps you, please give the warehouse a Start!