from dotenv import load_dotenv
import os

load_dotenv()
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

files = os.listdir("game_data")
file_texts = []
for file in files:
    with open(f"game_data/{file}") as f:
        file_text = f.read()
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=64,
    )
    texts = text_splitter.split_text(file_text)
    for i, chunked_text in enumerate(texts):
        file_texts.append(Document(page_content=chunked_text,
                                    metadata={"doc_title": file.split(".")[0], "chunk_num": i}))

embeddings = HuggingFaceEmbeddings()

vector_store = FAISS.from_documents(
    file_texts,
    embedding=embeddings
)

from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
llm = OctoAIEndpoint(
        model="meta-llama-3-8b-instruct",
        max_tokens=1024,
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9,
    )

from langchain.prompts import ChatPromptTemplate
template = """You are a chat filter system for an online game. Respond with 'toxic' if the prompt is toxic/rude and 'not toxic' if the prompt is not toxic/rude.
Question: {question}
Context: {context}
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

retriever = vector_store.as_retriever()

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
self.chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def LLM_moderate(self, msg):
    if self.chain is None:
        return("Moderator is not initialized, please wait!")
    result = self.chain.invoke(msg)
    return result
