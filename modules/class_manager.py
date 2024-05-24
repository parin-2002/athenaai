from modules.document_extractor import DocumentExtractor
from modules.chroma_vector_store import ChromaVectorStore
from modules.question_answer_chain import QuestionAnswerChain

# A main class to manage all other classes
class ClassManager:
    def __init__(self):
        pass

    def manage_document_extractor(self, all_docs):
        # Create an instance of DocumentExtractor
        doc_extractor = DocumentExtractor()
        # Call the get_text method to extract text from the documents
        self.extracted_documents, self.file_names = doc_extractor.get_text(all_docs)

    def manage_chroma_vector_store(self):
        # Create a ChromaVectorStore instance with specified model and persist directory.
        self.chroma_vector_store = ChromaVectorStore(model="text-embedding-3-large", persist_directory="./chroma_db")
        # Generate the Chroma vector store by processing the extracted documents.
        self.chroma_vector_store.create_vectorstore(self.extracted_documents)
        # Retrieve the generated Chroma vector store for further use.
        self.vectorstore = self.chroma_vector_store.get_vectorstore()
        # Create a retriever from the Chroma vector store with specified search arguments
        self.base_retriever = self.chroma_vector_store.as_retriever(search_kwargs={"k": 5})
        self.ensemble_retriever = self.chroma_vector_store.bm25Retriever()

    def manage_question_answer_chain(self,model_name):
        # Create an instance of QuestionAnswerChain
        self.question_answer_chain = QuestionAnswerChain(model_name=model_name)
        # call create_qa_chain to get question_answer_chain
        self.question_answer_chain.create_qa_chain(retriever=self.base_retriever)
        self.question_answer_chain.ensemble_retriever(self.ensemble_retriever)
        # call create_map_reduce_chain
        self.question_answer_chain.create_map_reduce_chain()
        # call create_generate_evaluate_mcq_chain
        self.question_answer_chain.create_generate_evaluate_mcq_chain()
        # add generated mcq to mcqs
        self.mcqs = None

    def answer_question(self, question):
        return self.question_answer_chain.answer_question(question)
    
    def ensemble_qa(self, que):
        return self.question_answer_chain.get_answer(que)
    
    def write_summary(self, file_name):
        chunks, text = self.chroma_vector_store.get_document(file_name)
        summary = self.question_answer_chain.summarize_text_map_reduce(chunks)
        # self.question_answer_chain.create_refinement_chain()
        # summary1=self.question_answer_chain.refine_summary(chunks)
        return summary
    
    def mcq_generator(self, file_name, number, subject, tone, response_json):
        chunks, text = self.chroma_vector_store.get_document(file_name)
        response = self.question_answer_chain.generate_and_evaluate_quiz(text, number, subject, tone, response_json)
        return response

Manager = None

def setManager():
    global Manager
    Manager = ClassManager()
    return Manager

def getManager():
    global Manager
    return Manager
