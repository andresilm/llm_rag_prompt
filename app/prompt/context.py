import glob
import os
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import uuid

from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.prompt.cohere import COHERE_API_KEY
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

DOCUMENTS_PATH = 'app/documents'
COLLECTION_NAME = 'code_challenge_docs'


class PromptContext:
    def __init__(self):
        self.__chroma_client = chromadb.PersistentClient(
            path="chromadb",
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )
        self._collection = self.retrieve_collection()
        self.__add_docs_in_folder(DOCUMENTS_PATH)

    def retrieve_collection(self):
        encode = embedding_functions.CohereEmbeddingFunction(api_key=COHERE_API_KEY, model_name="large")
        metadata_options = {
            "hnsw:space": "cosine"  # or "cosine"
        }
        encode = embedding_functions.CohereEmbeddingFunction(api_key=COHERE_API_KEY)
        collection = self.__chroma_client.get_or_create_collection(name=COLLECTION_NAME,
                                                                   metadata=metadata_options,
                                                                   embedding_function=encode)

        return collection

    def __add_docs_in_folder(self, folder: str):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=200, chunk_overlap=30)
        files = glob.glob(folder + os.sep + "*.txt")

        documents = []
        ids = []

        for filename in files:
            with open(filename, 'r') as _file:
                content = _file.read()
                docs = text_splitter.create_documents([content])
                for doc in docs:
                    uuid_name = uuid.uuid1()
                    ids.append(str(uuid_name))
                    documents.append(doc.page_content)

        self._collection.add(documents=documents, ids=ids)

    def get_context(self, question):
        similar_chunk = self._collection.query(query_texts=[question], n_results=1)['documents'][0]
        print(similar_chunk)
        return similar_chunk
