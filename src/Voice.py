import aiohttp
import aiofiles
import os
from dotenv import load_dotenv

load_dotenv()

class Voice:
    def __init__(self, uid="001") -> None:
        self.Emotion = "default"
        self.uid = uid
        self.apikey = os.getenv("AZURE_API_KEY")
        # 使用绝对路径或项目根目录相对路径
        self.audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '/', 'Audio'))
    
    async def get_voice(self, input: str):
        headers = {
            "Ocp-Apim-Subscription-Key": self.apikey,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "AI-arvter",
        }
        body = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-cn">
        <voice name="zh-CN-YunzeNeural">
            <mstts:express-as style="{self.Emotion}" role="SeniorMale" styledegree="2">
                {input}
            </mstts:express-as>
        </voice>
    </speak>"""

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://westus2.tts.speech.microsoft.com/cognitiveservices/v1",
                headers=headers,
                data=body.encode("utf-8"),
            ) as response:
                if response.status == 200:
                    content = await response.read()
                    os.makedirs(self.audio_dir, exist_ok=True)  # 确保目录存在
                    file_path = os.path.join(self.audio_dir, f"{self.uid}.mp3")
                    async with aiofiles.open(file_path, "wb") as audio:
                        await audio.write(content)
                    return file_path
                else:
                    print(f"Error: {response.status}")
                    return None
