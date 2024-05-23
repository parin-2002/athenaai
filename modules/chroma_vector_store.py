from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import BM25Retriever, EnsembleRetriever

class ChromaVectorStore:
    def __init__(self, model="text-embedding-3-large", persist_directory=None):
        """
        Initialize ChromaVectorStore instance.
        
        Args:
            model (str): Name of the OpenAI model to use for embeddings.
            persist_directory (str): Directory to persist Chroma vector store.
        """
        self.model = model
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model=self.model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=16, length_function=len)
        self.vectorstore = None

    def create_vectorstore(self, all_docs):
        """
        Create Chroma vector store from input documents.

        Args:
            all_docs (list): List of documents to generate vector store from.
        """
        self.docs = self.text_splitter.split_documents(all_docs)
        # create simple ids
        ids = [str(i) for i in range(1, len(self.docs) + 1)]
        self.vectorstore = Chroma.from_documents(self.docs, self.embeddings, ids=ids)

    def get_vectorstore(self):
        """
        Get the Chroma vector store.

        Returns:
            vectorstore: Chroma vector store generated from input documents.
        """
        return self.vectorstore
    
    def as_retriever(self, search_kwargs):
        """
        Create a retriever from the Chroma vector store.

        Args:
            search_kwargs (dict): Keyword arguments for retrieval.

        Returns:
            BaseRetriever: Retriever object.
        """
        if self.vectorstore is None:
            raise ValueError("Vector store has not been created. Please call create_vectorstore() method first.")
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    def bm25Retriever(self):
        """
        Create an Ensemble retriever using BM25 and Chroma retrievers.

        Returns:
            EnsembleRetriever: An ensemble retriever combining BM25 and Chroma retrievers.
        """
        bm25_retriever = BM25Retriever.from_documents(self.docs)
        bm25_retriever.k = 3
        chroma_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, chroma_retriever], weights=[0.42, 0.58])
        return ensemble_retriever
    
    def get_document(self, file_name):
        docs = self.vectorstore.get(where={'Name': file_name})['documents']
        text = ""
        for doc in docs:
            text += doc
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
        chunks = text_splitter.create_documents([text])
        return chunks, text

# Example usage:
# all_docs = [...]  # Your list of documents
# chroma_vector_store = ChromaVectorStore(model="text-embedding-ada-002", persist_directory="./chroma_db")
# chroma_vector_store.create_vectorstore(all_docs)
# vectorstore = chroma_vector_store.get_vectorstore()
# Create a retriever from the Chroma vector store with specified search arguments
# base_retriever = chroma_vector_store.as_retriever(search_kwargs={"k": 5})
