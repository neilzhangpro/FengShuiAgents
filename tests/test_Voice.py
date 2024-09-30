import unittest
from unittest.mock import patch, mock_open
import os
from src.Voice import Voice

class TestVoice(unittest.TestCase):

    def setUp(self):
        # 在每个测试方法之前运行
        self.voice = Voice()
        self.voice.uid = "test_uid"
        self.voice.Emotion = "cheerful"

    def test_init(self):
        # 测试初始化
        self.assertIsNotNone(self.voice.Emotion)
        self.assertIsNotNone(self.voice.uid)
        self.assertEqual(self.voice.apikey, os.getenv("AZURE_API_KEY"))

    @patch('voice.requests.post')
    @patch('builtins.open', new_callable=mock_open)
    async def test_get_voice_success(self, mock_file, mock_post):
        # 模拟成功的 API 响应
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b"audio content"
        mock_post.return_value = mock_response

        # 调用方法
        await self.voice.get_voice("测试文本")

        # 验证 API 调用
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "https://westus2.tts.speech.microsoft.com/cognitiveservices/v1")
        self.assertIn("Ocp-Apim-Subscription-Key", call_args[1]['headers'])
        self.assertIn("测试文本", call_args[1]['data'].decode('utf-8'))

        # 验证文件写入
        mock_file.assert_called_once_with("test_uid.mp3", "wb")
        mock_file().write.assert_called_once_with(b"audio content")

    @patch('voice.requests.post')
    async def test_get_voice_failure(self, mock_post):
        # 模拟失败的 API 响应
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # 调用方法
        await self.voice.get_voice("测试文本")

        # 验证没有文件写入操作
        with self.assertRaises(FileNotFoundError):
            with open("test_uid.mp3", "rb") as f:
                pass

    def test_emotion_setting(self):
        # 测试情绪设置
        self.voice.Emotion = "angry"
        self.assertEqual(self.voice.Emotion, "angry")

    def test_uid_setting(self):
        # 测试 UID 设置
        self.voice.uid = "new_uid"
        self.assertEqual(self.voice.uid, "new_uid")
