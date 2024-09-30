import os
os.environ['USER_AGENT'] = 'FengShuiAgents/1.0'
import unittest
from unittest.mock import patch, MagicMock
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from src.AddDoc import AddDocClass

class TestAddDocClass(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.add_doc = AddDocClass()
    
    async def asyncTearDown(self):
        del self.add_doc
    
    async def test_init(self):
        self.assertIsInstance(self.add_doc.embeddings, OpenAIEmbeddings)
        self.assertIsInstance(self.add_doc.loader(["http://example.com"]), WebBaseLoader)
        self.assertIsInstance(self.add_doc.splitter, RecursiveCharacterTextSplitter)
        self.assertIsInstance(self.add_doc.qdrant, QdrantVectorStore)

    @patch('src.AddDoc.WebBaseLoader')
    async def test_add_urls(self, mock_webloader):
        mock_webloader_instance = MagicMock()
        mock_webloader_instance.load.return_value = ["mocked docs"]
        mock_webloader.return_value = mock_webloader_instance
        #切分文档
        mock_splitter = MagicMock()
        mock_splitter.split_documents.return_value = ["splitted docs"]
        #注意mock_splitter是AddDocClass的一个属性
        self.add_doc.splitter = mock_splitter
        #mock qdrant
        mock_qdrant = MagicMock()
        mock_qdrant.add_documents.return_value = {"ok": "urls添加成功"}
        self.add_doc.qdrant = mock_qdrant

        urls = ["http://example.com"]
        #调用add_urls方法
        await self.add_doc.add_urls(urls)
        #验证调用
        mock_webloader.assert_called_once_with(urls)
        mock_webloader_instance.load.assert_called_once_with()
        #验证切分文档
        mock_splitter.split_documents.assert_called_once_with(["mocked docs"])
        #验证添加文档
        mock_qdrant.add_documents.assert_called_once_with(["splitted docs"])


