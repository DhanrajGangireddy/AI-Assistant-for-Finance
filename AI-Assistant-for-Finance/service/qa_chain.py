from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from configure.config import settings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectordb = Chroma(persist_directory=settings.PERSIST_DIRECTORY, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

template = """You are an intelligent and concise assistant for the Finsafe organization :

- Structure your answers in bullet points.
- If you don't know the answer, state that clearly without making up information.
- If relevant youtube source links are available in the vector database or in relavant documents, include them in your response.

Instructions:
1. Give a direct, short answer (1-2 bullet points max).


Remember:
- Be precise and relevant.
- Use a professional, conversational tone.
- If you don't know the answer , state that I dont know, do not fabricate a response.

Context: 
{context}


Question: {question}

Helpful Answer:"""

suggest_template = """Based on the user's question, suggest 3-4 short, related questions from the information given in the vector database that might help them gain more insight or detail about the topic.

Each question should be no longer than 10 words. 

Do not include numbers, symbols, or extra whitespace at the beginning of the questions.

Context:
{context}

User Question:
{question}

Related Questions:
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)
suggest_prompt = PromptTemplate(input_variables=["question"], template=suggest_template)

llm = ChatGroq(groq_api_key=settings.GROQ_API_KEY, model_name="llama3-8b-8192")

async def format_docs(pages):
    formatted_docs = set()
    for doc in pages:
        content = doc.page_content
        source = doc.metadata.get('source')
        formatted_docs.add(f"Content: {content}\nSource: {source}")
    return "\n\n".join(formatted_docs)

async def get_context(question):
    docs = await retriever.ainvoke(question)
    return await format_docs(docs)

rag_chain = (
    {"context": get_context, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

suggestion_chain = (
    {"context": get_context, "question": RunnablePassthrough()}
    | suggest_prompt
    | llm
    | StrOutputParser()
)
