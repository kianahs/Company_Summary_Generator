import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from datetime import datetime

load_dotenv()


def chunk_data(dir_path, splitter):
    documents = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".md"):
            file_path = os.path.join(dir_path, file_name)
            raw_documents = TextLoader(file_path, encoding="utf-8").load()
            for item in raw_documents:
                item.metadata['source'] = file_name
                documents.append(item)

    return splitter.split_documents(documents)


def build_vector_store(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)


def choose_llm(free_plan):
    if free_plan:
        return ChatGroq(
            model_name="llama3-70b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        ), "llama3-70b-8192"
    else:
        return ChatOpenAI(
            model="gpt-4.1-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        ), "gpt-4.1-mini"


def execute_RAG_pipeline(dir_path, output_dir, free_plan):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    chunked_data = chunk_data(dir_path, splitter)
    print("Number of chunks:", len(chunked_data))

    vector_store = build_vector_store(chunked_data, embeddings)
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 10})

    llm, model_name = choose_llm(free_plan)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, chain_type="stuff"
    )

    current_date = datetime.now().strftime("%B %Y")
    section_queries = {
        "Company Description": "What is the company’s mission, purpose, and values?",
        "Products & Services": "What products and services does the company offer? What problems do they solve?",
        "Notable Customers or Company Mentions": "List any companies or partners mentioned and describe their relationship (e.g., customer, partner, etc).",
        "Leadership Team": "Who are the key leaders in the company? Include names, roles, and short bios if available.",
        "Recent News": f"What are the 10 recent news, blog posts, or updates mentioned on the site? (current date is {current_date})"
    }

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, f"RAG_Company_Summary_{model_name}.md"), "w", encoding="utf-8") as f:
        for title, query in section_queries.items():
            f.write(f"## {title}\n")
            summary = qa_chain.run(query)
            f.write(summary + "\n\n")


if __name__ == "__main__":
    execute_RAG_pipeline("Outputs/filament/Cleaned Scraped Data",
                         "Outputs/filament/Final Summary/RAG", True)
