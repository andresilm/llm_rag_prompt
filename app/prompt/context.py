import glob
import os
import chromadb
import uuid
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

logger = logging.getLogger(__name__)

DOCUMENTS_PATH = 'app/documents'
COLLECTION_NAME = 'code_challenge_docs'


class PromptContext:
    def __init__(self, cohere_client):
        self.__cohere_client = cohere_client
        self.__chroma_client = chromadb.PersistentClient(
            path="chromadb",
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )
        self._collection = self.retrieve_collection()
        self.__add_docs_in_folder(DOCUMENTS_PATH)

    def retrieve_collection(self):
        return self.__chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    def __add_docs_in_folder(self, folder: str):
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n"], chunk_size=256, chunk_overlap=100)
        files = glob.glob(folder + os.sep + "*.txt")
        documents = []
        ids = []
        embeddings = []
        for filename in files:
            with open(filename, 'r') as _file:
                content = _file.read()
                docs = text_splitter.create_documents([content])
                for doc in docs:
                    uuid_name = str(uuid.uuid1())
                    response = self.__cohere_client.embed(texts=[doc.page_content],
                                                          model='embed-multilingual-light-v3.0',
                                                          input_type="search_query")
                    embedding = response.embeddings[0]
                    embedding = embedding.tolist() if hasattr(embedding, 'tolist') else embedding
                    logger.info(f'Will add document:\n<{doc.page_content}>\nembedding length = {len(embedding)}')
                    documents.append(doc.page_content)
                    ids.append(uuid_name)
                    embeddings.append(embedding)

        self._collection.upsert(documents=documents, ids=ids, embeddings=embeddings)

    def get_context(self, question):
        response = self.__cohere_client.embed(texts=[question],
                                              model='embed-multilingual-light-v3.0',
                                              input_type="search_query")
        input_embedding = response.embeddings[0]
        similar_chunk = self._collection.query(query_embeddings=[input_embedding], n_results=1)['documents'][0]
        logger.info(f'Most relevant document:\n{similar_chunk}')
        return similar_chunk
