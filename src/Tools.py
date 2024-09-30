from langchain.agents import AgentExecutor,create_tool_calling_agent,tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate   
import os
import requests
from dotenv import load_dotenv
load_dotenv()
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")

@tool
def search(query: str) -> str:
    """只有需要了解实时信息或不知道的事情的时候才会使用这个工具."""
    serp = SerpAPIWrapper()
    return serp.run(query)

@tool
def get_info_from_local(query: str) -> str:
    """只有回答与2024年运势或龙年运势相关问题的时候会使用这个工具."""
    client = QdrantClient(path="/tmp/local_qdrant")
    retriever_qr = QdrantVectorStore(client, "local_documents_demo", OpenAIEmbeddings())
    retriever = retriever_qr.as_retriever(search_type="mmr")
    result = retriever.get_relevant_documents(query)
    return result

@tool
def jiemeng(query: str):
    """只有帮助用户解梦的时候才会使用这个工具，需要输入梦境内容."""
    url = f"https://api.yuanfenju.com/index.php/v1/Gongju/zhougong"
    LLM = ChatOpenAI(
            model="gpt-4-1106-preview", 
            temperature=0, 
            streaming=True
        )
    prompt = ChatPromptTemplate.from_template("根据输入的内容提取1个关键词，只返回关键词，输入内容:{topic}")
    prompt_value = prompt.invoke({"topic": query})
    keyword = LLM.invoke(prompt_value)
    print("=======提交数据=======")
    print(keyword.content)
    result = requests.post(url, data={"api_key": os.getenv("API_KEY"), "title_zhougong": keyword.content})
    if result.status_code == 200:
        print("=======返回数据=======")
        return result.text
    else:
        return "用户输入的信息缺失，提醒用户补充信息！"