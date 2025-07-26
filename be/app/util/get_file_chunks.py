from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def read_text_file(file_path: str):
    loader = TextLoader(file_path)
    docs = loader.load()
    return docs

def split_docs(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    return chunks

def get_file_chunks(file_path: str):
    docs = read_text_file(file_path)
    chunks = split_docs(docs)
    return chunks





