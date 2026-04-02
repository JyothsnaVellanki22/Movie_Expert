from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings

app = FastAPI(title="Star Wars RAG API", description="API for Star Wars RAG Bot")

# Add CORS middleware to allow the React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Configs matching main.py
PERSIST_PATH = "./qdrant_db"
COLLECTION_NAME = "star-wars"

# Initialize Models identically to main.py
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536,
    encoding_format="float32",
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Initialize Qdrant Client
# We simply load the existing database that main.py populated
client = QdrantClient(path=PERSIST_PATH)
vectorstore = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

# Setup Retriever & Chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

template = """
you are a helpful assistant that answers questions about Star Wars movies.
Use the following context to answer the question.
If you don't know the answer, say so.

Context: {context}
Question: {question}
Answer: 
""" 

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # We use ainvoke for asynchronous execution, making the API efficient
        response = await rag_chain.ainvoke(request.message)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
