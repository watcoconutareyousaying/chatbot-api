from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# extract text from pdf files


def load_pdf_file(data):
    loader = DirectoryLoader(
        data, glob="*.pdf", loader_cls=PyPDFLoader)  # type: ignore
    documents = loader.load()
    return documents

# split text into chunks


def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# download embeddings from huggingface.co
def download_huggingface_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings