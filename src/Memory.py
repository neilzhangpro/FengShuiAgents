from langchain.memory import ConversationTokenBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from src.Prompt import PromptClass
from dotenv import load_dotenv
load_dotenv()

class MemoryClass:
    def __init__(self,memorykey="chat_history",model="gpt-4o-mini"):
        self.memorykey = memorykey
        self.memory = []
        self.chatmodel = ChatOpenAI(model=model)

    def summary_chain(self,store_message):
        SystemPrompt = PromptClass().SystemPrompt
        Moods = PromptClass().MOODS
        prompt = ChatPromptTemplate.from_messages([
            ("system", SystemPrompt+"\n这是一段你和用户的对话记忆，对其进行总结摘要，摘要使用第一人称'我'，并且提取其中的用户关键信息，如用户姓名、生日、爱好等，以如下格式返回：\n 总结摘要|用户关键信息\n例如 用户张三问候我好，我礼貌回复，然后他问我今年运势如何，我回答了他今年的运势，然后他告辞离开。|张三,生日1990年1月1日"),
            ("user", "{input}")
        ])
        chain = prompt | self.chatmodel
        summary = chain.invoke({"input": store_message,"who_you_are":Moods["default"]["roloSet"]})
        return summary
    
    def get_memory(self):
        try:
            chat_message_history =RedisChatMessageHistory(
                url="redis://localhost:6379/0", session_id="session1"
            )
            # 对超长的聊天记录进行摘要
            store_message = chat_message_history.messages
            if len(store_message) > 10:
                str_message = ""
                for message in store_message:
                    str_message+=f"{type(message).__name__}: {message.content}"
                summary = self.summary_chain(str_message)
                chat_message_history.clear() #清空原有的对话
                chat_message_history.add_message(summary) #保存总结
                print("添加总结后:",chat_message_history.messages)
                return chat_message_history
            else:
                print("go to next step")
                return chat_message_history
        except Exception as e:
            print(e)
            return None

    def set_memory(self):
        self.memory = ConversationTokenBufferMemory(
            llm=self.chatmodel,
            human_prefix="user",
            ai_prefix="陈大师",
            memory_key=self.memorykey,
            output_key="output",
            return_messages=True,
            max_token_limit=1000,
            chat_memory=self.get_memory(),
        )
        return self.memory

    