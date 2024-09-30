import unittest
from unittest.mock import patch, MagicMock
from src.Agents import AgentClass
from src.Emotion import EmotionClass
from src.Tools import search
from langchain_openai import ChatOpenAI

class TestAgentsClass(unittest.TestCase):
    def setUp(self):
        self.master = AgentClass()
    
    def test_init(self):
        self.assertIsInstance(self.master.chatmodel,ChatOpenAI)
        self.assertEqual(self.master.tools,[search])
        self.assertEqual(self.master.memorykey,"chat_history")
        self.assertEqual(self.master.feeling,"default")
        self.assertIsNotNone(self.master.prompt)
        self.assertIsNotNone(self.master.memory)
        self.assertIsNotNone(self.master.feeling)
        self.assertIsInstance(self.master.emotion, EmotionClass)
        self.assertIsNotNone(self.master.agent)
        self.assertIsNone(self.master.agent_chain)

    @patch('src.Agents.AgentExecutor')
    def test_agent_run(self, MockAgentExecutor):
        # 创建一个模拟的 EmotionClass 实例
        mock_emotion_instance = MagicMock()
        mock_emotion_instance.Emotion_Sensing.return_value = "happy"
        
        # 将模拟的实例设置为 AgentClass 的 emotion 属性
        self.master.emotion = mock_emotion_instance

        # 设置 AgentExecutor 模拟返回值
        mock_agent_instance = MagicMock()
        MockAgentExecutor.return_value = mock_agent_instance

        # 调用 run_agent 方法
        self.master.run_agent("很高兴认识你!")

        # 验证 Emotion_Sensing 被正确调用
        mock_emotion_instance.Emotion_Sensing.assert_called_once_with("很高兴认识你!")
        
        # 验证 AgentExecutor 被正确创建
        MockAgentExecutor.assert_called_once_with(
            agent=self.master.agent,
            tools=self.master.tools,
            memory=self.master.memory,
            verbose=True
        )
        
        # 验证 AgentExecutor 的 invoke 方法被正确调用
        mock_agent_instance.invoke.assert_called_once_with({
            "input": "很高兴认识你!"
        })
        
        # 验证 feeling 属性被正确设置
        self.assertEqual(self.master.feeling, "happy")