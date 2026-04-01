import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536,
    encoding_format="float32",
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

PERSIST_PATH = "./qdrant_db"
COLLECTION_NAME = "star-wars"

def load_star_wars(url, movie_title):
    response = requests.get(url) # Fetch the HTML content from the URL
    soup = BeautifulSoup(response.content, 'html.parser') # Parse the HTML content
    script_raw = soup.find("pre").get_text() # Extract the text from the div with class 'mw-parser-output'
    
    return Document(page_content=script_raw, metadata={"title": movie_title}) # Return the extracted text as a Document object

def main():
    client = QdrantClient(path=PERSIST_PATH) # Initialize the Qdrant client
    
    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embeddings=embeddings,
        )
    except Exception:
        client.close()

    star_wars = [
            {
                "title": "Star Wars: A New Hope",
                "url": "https://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html",
            },
            {
                "title": "Star Wars: The Empire Strikes Back",
                "url": "https://www.imsdb.com/scripts/Star-Wars-The-Empire-Strikes-Back.html",
            },
            {
                "title": "Star Wars: Return of the Jedi",
                "url": "https://www.imsdb.com/scripts/Star-Wars-Return-of-the-Jedi.html",
            },    
        ]

    script_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        add_start_index=True,
        separators=["\nINT.", "\nEXT.", "\n\n", "\n", " ", ""],
    )

    all_chunks = []

    for script in star_wars:
        doc = load_star_wars(script["url"], script["title"])
        chunks = script_splitter.split_documents([doc])
        all_chunks.extend(chunks)
        print(
            f"Loaded and split script for {script['title']} into {len(chunks)} chunks from {len(star_wars)} movies"
        )
    
    vectorstore = QdrantVectorStore.from_documents(
        all_chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        path=PERSIST_PATH,
    )

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
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    print("\n--- Star Wars RAG Bot is ready to go! ---")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = rag_chain.invoke(query)
        print(f"\nBot: {response}")

if __name__ == "__main__":
    main()
