import os
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import json
from pathlib import Path
from db_utils import dump_db_to_json


dump_db_to_json()

template = """Sei un sistema intelligente di gestione dell'inventario di casa mia. Rispondi alla domanda basandoti sul seguente contesto:

{context}

Domanda: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

file_path='output.json'
data = json.loads(Path(file_path).read_text())

documents = [Document(page_content=x["product_name"], metadata={key: value for key, value in x.items() if key != "product_name"}) for x in data]
# db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory="chromadb")
if os.path.exists("chromadb"):
    print(f"Directory chromadb exists. Using existing vectordb")
    db = Chroma(persist_directory="chromadb", embedding_function=OpenAIEmbeddings())

else:
    print(f"Directory chromadb does not exist. Creating new vectordb")
    db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory="chromadb")
    db.persist()

def format_docs(docs):
    formatted_docs = ""
    for d in docs:
        formatted_docs += f"\n\nproduct name: {d.page_content}\n"
        for m in d.metadata.items():
            formatted_docs += f"{m[0].replace('_', ' ')}: {m[1]}\n"

    return formatted_docs

retriever = db.as_retriever()
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

