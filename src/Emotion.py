from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

class EmotionClass:
    def __init__(self,model="gpt-4o-mini"):
        self.chat = None
        self.Emotion = None
        self.chatmodel = ChatOpenAI(model=model)

    def Emotion_Sensing(self, input):
        # 处理输入长度
        original_input = input
        if len(input) > 100:
            input = input[:100]
            print(f"Input is too long, only the first 100 characters will be used. Original length: {len(original_input)}")
        
        print(f"Processing input: {input}")
        
        # 定义 JSON schema
        json_schema = {
            "title": "emotions",
            "description": "feedback emotions",
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "the user input",
                    "minLength": 1,
                    "maxLength": 100
                },
                "output": {
                    "type": "string",
                    "description": "the emotion of the user input",
                    "enum": ["depressed", "friendly", "default", "angry", "cheerful"]
                }
            },
            "required": ["input", "output"],
        }
        llm = self.chatmodel.with_structured_output(json_schema)
        
        prompt_emotion = """
        根据用户的输入判断用户的情绪,回应规则对照下面：
        1. 内容为负面情绪，只返回"depressed"，不要有其他内容，例如压抑、抑郁的语句.
        2. 内容为正面情绪，只返回"friendly"，不要有其他内容，例如友好的、礼貌的语句.
        3. 内容为中性情绪，只返回"default"，不要有其他内容.
        4. 内容为愤怒生气情绪的内容，只返回"angry"，不要有其他内容，例如愤怒、辱骂、笨蛋、仇恨的语句.
        5. 内容包含情绪十分开心，只返回"cheerful"，不要有其他内容，例如高兴的、狂喜的、兴奋、称赞的语句.
        用户输入内容:{input}
        """
        
        # 模拟情绪链
        EmotionChain = ChatPromptTemplate.from_messages([("system", prompt_emotion), ("user", input)]) | llm
        
        try:
            if not input.strip():
                print("Empty input received")
                return None
            
            if EmotionChain is not None:
                result = EmotionChain.invoke({"input": input})
                print(f"API response: {result}")
            else:
                raise ValueError("EmotionChain is not properly instantiated.")
            
            self.Emotion = result["output"]
            return result["output"]
        except Exception as e:
            print(f"Error in Emotion_Sensing: {str(e)}")
            return None
