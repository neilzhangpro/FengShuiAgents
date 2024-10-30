from langchain.agents import AgentExecutor,create_tool_calling_agent,tool
from langchain_openai import ChatOpenAI
from .Prompt import PromptClass
from .Memory import MemoryClass
from .Emotion import EmotionClass
from .Tools import *
from dotenv import load_dotenv
load_dotenv()
import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")





class AgentClass:
    def __init__(self):
        self.modelname = "gpt-4o-mini"
        self.chatmodel = ChatOpenAI(model=self.modelname)
        self.tools = [search]
        self.memorykey = "chat_history"
        self.feeling = "default"
        self.prompt = PromptClass(memorykey=self.memorykey,feeling=self.feeling).Prompt_Structure()
        self.memory = MemoryClass(memorykey=self.memorykey,model=self.modelname).set_memory()
        self.emotion = EmotionClass(model=self.modelname)
        self.agent = create_tool_calling_agent(
            self.chatmodel,
            self.tools,
            self.prompt,
        )
        self.agent_chain = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    

    def run_agent(self,input):
        # run emotion sensing
        self.feeling = self.emotion.Emotion_Sensing(input)
        self.prompt = PromptClass(memorykey=self.memorykey,feeling=self.feeling).Prompt_Structure()
        print(self.feeling)
        print(self.prompt)
        res = self.agent_chain.invoke({
            "input": input,
        })
        return res
    
    async def run_agent_ws(self,input):
        # run emotion sensing
        self.feeling = self.emotion.Emotion_Sensing(input)
        self.prompt = PromptClass(memorykey=self.memorykey,feeling=self.feeling).Prompt_Structure()
        async for event in self.agent_chain.astream_events({"input": input,"chat_history":self.memory},version="v2"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="|")
                    yield content           
        
