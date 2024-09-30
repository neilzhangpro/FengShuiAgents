import tempfile
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

class AddDocClass:
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings()
        self.loader = lambda urls: WebBaseLoader(urls)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
        
         # 创建一个唯一的临时目录
        self.temp_dir = tempfile.mkdtemp(prefix="qdrant_")
        client = QdrantClient(path=self.temp_dir)
        
        collection_name = "local_documents_demo"
        
        # 检查集合是否存在，如果不存在则创建
        collections = client.get_collections().collections
        if not any(collection.name == collection_name for collection in collections):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        self.qdrant = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=self.embeddings,
        )

    async def add_urls(self, urls: list) -> None:
        loader = self.loader(urls)
        docs = loader.load()
        documents = self.splitter.split_documents(docs)
        self.qdrant.add_documents(documents)
        return {"ok": "urls添加成功"}

    def __del__(self):
        # 清理临时目录
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
