from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
texts = [
    "Hello this is Mukesh Prajapati",
    "Hello your name is Youtube",
    "And you all are very beautiful"
]
vector = embeddings.embed_documents(texts)

print(vector)
