import unittest
from src.Emotion import EmotionClass


class TestEmotionClass(unittest.TestCase):

    def setUp(self):
        self.master = EmotionClass()

    def test_init(self):
        self.assertIsNone(self.master.Emotion)
        self.assertIsNotNone(self.master.chatmodel)

    def test_emotion_sensing_positive(self):
        input_list = ["我今天很高兴啊", "这真是太棒了", "我感到非常开心"]
        expected_emotions = ["friendly", "cheerful"]
        for input in input_list:
            results = [self.master.Emotion_Sensing(input) for _ in range(3)]
            self.assertTrue(any(result in expected_emotions for result in results),
                          f"对于积极输入 '{input}', 没有返回积极情绪!")

    def test_emotion_sensing_negative(self):
        input_list = ["我今天很难过", "这真是太糟糕了", "我感到非常沮丧"]
        expected_emotions = ["depressed"]
        for input in input_list:
            results = [self.master.Emotion_Sensing(input) for _ in range(3)]
            self.assertTrue(any(result in expected_emotions for result in results),f"对于消极输入 '{input}', 没有返回消极情绪!")

    def test_emotion_sensing_neutral(self):
        input_list = ["正在写作业", "我刚吃完午饭", "明天我要去上班"]
        expected_emotions = ["default"]
        for input in input_list:
            result = self.master.Emotion_Sensing(input)
            results = [self.master.Emotion_Sensing(input) for _ in range(3)]
            self.assertTrue(any(result in expected_emotions for result in results),
                          f"对于中性输入 '{input}', 没有返回中性情绪!")

    def test_emotion_sensing_angry(self):
        input_list = ["你这个笨蛋！", "滚开！", "我恨你"]
        expected_emotions = ["angry"]
        for input in input_list:
            result = self.master.Emotion_Sensing(input)
            results = [self.master.Emotion_Sensing(input) for _ in range(3)]
            self.assertTrue(any(result in expected_emotions for result in results),
                          f"对于愤怒输入 '{input}', 没有返回愤怒情绪!")


    def test_emotion_sensing_empty(self):
        input = ""
        result = self.master.Emotion_Sensing(input)
        self.assertIsNone(result, None)
    
    def test_emotion_sensing_longinput(self):
        input = "我今天很高兴啊" * 1000
        result = self.master.Emotion_Sensing(input)
        self.assertIsNotNone(result, "长输入没有返回结果")
        self.assertIn(result, ["friendly", "cheerful"], f"长输入返回了意外的结果: {result}")


if __name__ == '__main__':
    unittest.main()
