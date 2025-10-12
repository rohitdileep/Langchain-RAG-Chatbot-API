from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader , PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
import os , shutil
from typing import List
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="./db", embedding_function=embedding_function)

def get_chunks(folder_path : str)->List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            loader = Docx2txtLoader(os.path.join(folder_path, filename))
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, filename))
        else:
            print(f"Unsupported file format: {filename}")
        docs = loader.load()
        documents.extend(docs)
    docs = text_splitter.split_documents(documents)
    return docs




def get_vectorstore(folder_path : str , file_id : int):
    chunks = get_chunks(folder_path)
 

    # vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory='db', collection_name='company_history')
    try:
        for split in chunks:
            split.metadata['file_id'] = file_id
        vectordb.add_documents(chunks, collection_name="company_history")
        print(f"Added {len(chunks)} chunks for file_id={file_id}")
        return True
    except Exception as e:
        raise Exception(f"Error adding documents to vector store: {e}")
    
   
    


def delete_vectorstore(file_id : int)->bool:

    try:
        docs =  vectordb.get(where={"file_id" : file_id})
        print(f'Found {len(docs)} documents to delete for file_id {file_id}')
        vectordb._collection.delete(where={"file_id": file_id})
        print(f'Deleted documents for file_id {file_id}')
        return True
    
    except:
        print(f'No documents found for file_id {file_id} or error occurred')
        return False



    