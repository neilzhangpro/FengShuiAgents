import unittest
from unittest.mock import patch, MagicMock
from src.Memory import MemoryClass

class TestMemoryClass(unittest.TestCase):

    def setUp(self):
        self.memory_class = MemoryClass()

    @patch('src.Memory.ChatOpenAI')
    def test_init(self, MockChatOpenAI):
        memory = MemoryClass(memorykey="test_key", model="test-model")
        self.assertEqual(memory.memorykey, "test_key")
        self.assertEqual(memory.memory, [])
        MockChatOpenAI.assert_called_once_with(model="test-model")

    @patch('src.Memory.PromptClass')
    @patch('src.Memory.ChatPromptTemplate')
    def test_summary_chain(self, MockChatPromptTemplate, MockPromptClass):
        mock_prompt = MagicMock()
        MockChatPromptTemplate.from_messages.return_value = mock_prompt
        
        mock_chain = MagicMock()
        mock_prompt.__or__.return_value = mock_chain
        mock_chain.invoke.return_value = "摘要|关键信息"

        MockPromptClass.return_value.SystemPrompt = "系统提示"
        MockPromptClass.return_value.MOODS = {"default": {"roloSet": "角色设定"}}

        result = self.memory_class.summary_chain("测试消息")
        
        self.assertEqual(result, "摘要|关键信息")
        mock_chain.invoke.assert_called_once_with({"input": "测试消息", "who_you_are": "角色设定"})

    @patch('src.Memory.RedisChatMessageHistory')
    def test_get_memory_short_history(self, MockRedisChatMessageHistory):
        mock_history = MagicMock()
        mock_history.messages = [MagicMock() for _ in range(5)]
        MockRedisChatMessageHistory.return_value = mock_history

        result = self.memory_class.get_memory()
        
        self.assertEqual(result, mock_history)


    @patch('src.Memory.RedisChatMessageHistory')
    @patch.object(MemoryClass, 'summary_chain')
    def test_get_memory_long_history(self, mock_summary_chain, MockRedisChatMessageHistory):
        mock_history = MagicMock()
        mock_history.messages = [MagicMock(content="消息内容") for _ in range(11)]
        MockRedisChatMessageHistory.return_value = mock_history

        mock_summary_chain.return_value = "摘要|关键信息"

        result = self.memory_class.get_memory()
        
        self.assertEqual(result, mock_history)
        mock_history.clear.assert_called_once()
        mock_history.add_message.assert_called_once_with("摘要|关键信息")

    @patch('src.Memory.ConversationTokenBufferMemory')
    @patch.object(MemoryClass, 'get_memory')
    def test_set_memory(self, mock_get_memory, MockConversationTokenBufferMemory):
        mock_memory = MagicMock()
        MockConversationTokenBufferMemory.return_value = mock_memory

        mock_chat_memory = MagicMock()
        mock_get_memory.return_value = mock_chat_memory

        result = self.memory_class.set_memory()

        self.assertEqual(result, mock_memory)
        self.assertEqual(self.memory_class.memory, mock_memory)
        MockConversationTokenBufferMemory.assert_called_once_with(
            llm=self.memory_class.chatmodel,
            human_prefix="user",
            ai_prefix="陈大师",
            memory_key=self.memory_class.memorykey,
            output_key="output",
            return_messages=True,
            max_token_limit=1000,
            chat_memory=mock_chat_memory
        )


