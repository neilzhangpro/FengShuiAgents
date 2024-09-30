import unittest
from unittest.mock import patch, MagicMock
from src.Prompt import PromptClass
from langchain_core.prompts import ChatPromptTemplate  # 添加这个导入

class TestPromptClass(unittest.TestCase):
    
        def setUp(self):
            self.prompt = PromptClass()
        @patch("langchain_core.prompts.ChatPromptTemplate")
        def test_prompt_structure(self,mock_chat_prompt_template):
            prompt = self.prompt.Prompt_Structure()
            #验证返回的是ChatPromptTemplate
            self.assertIsInstance(prompt,ChatPromptTemplate)

        def test_prompt_with_feeling(self):
             self.prompt.feeling = "friendly"
             prompt = self.prompt.Prompt_Structure()
             self.assertIn("你现在感到十分温暖和友好", str(prompt))
