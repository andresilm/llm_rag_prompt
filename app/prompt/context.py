import chromadb
from chromadb.utils import embedding_functions
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.prompt.cohere import COHERE_API_KEY


class PromptContext:
    def __init__(self, collection_name):
        self.__collection_name = collection_name
        self.__chroma_client = chromadb.Client()
        self.__collection = self.retrieve_collection(self.__chroma_client, self.__collection_name)

    @staticmethod
    def retrieve_collection(chroma_client, collection_name):
        cohere_ef = embedding_functions.CohereEmbeddingFunction(api_key=COHERE_API_KEY,  model_name="large")
        metadata_options = {
            "hnsw:space": "ip"  # You can change this to "ip" or "cosine" if needed
        }

        collection = chroma_client.get_or_create_collection(name=collection_name,
                                                            metadata=metadata_options,
                                                            embedding_function=cohere_ef)

        return collection

    def add_docs_to_collection(self, content):
        text_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n"], chunk_size=200, chunk_overlap=30)

        docs = text_splitter.create_documents([content])
        for doc in docs:
            uuid_name = uuid.uuid1()
            print("document for", uuid_name)
            self.__collection.add(ids=[str(uuid_name)], documents=doc.page_content)

    def get_context(self, question):
        return self.__collection.query(query_texts=[question], n_results=1)['documents'][0]
