import os 
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS 
from langchain.chains.question_answering import load_qa_chain 
from langchain.agents import AgentType, initialize_agent, Tool 
from langchain.memory import ConversationBufferMemory 
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.tools import DuckDuckGoSearchResults 
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

def create_vector_store(pdf_path: str) -> FAISS:
    # Load the PDF file from the root folder 
    loader = PyPDFLoader(pdf_path) 
    documents = loader.load() # load full document 
    
    # Split document into chunks for better processing 
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    # Initialize embeddings with Azure OpenAI parameters from the .env file 
    embedding = AzureOpenAIEmbeddings(deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"))
    
    # Create and return a FAISS vector store from the document chunks 
    vectorstore = FAISS.from_documents(docs, embedding) 
    return vectorstore 

def vector_search(query: str, vectorstore: FAISS, llm: AzureChatOpenAI) -> str:
    # Retrieve relevant documents based on similarity search 
    docs = vectorstore.similarity_search(query) 
    
    # Load a simple QA chain ("stuff" chain type) to synthesize an answer 
    qa_chain = load_qa_chain(llm, chain_type="stuff") 
    answer = qa_chain.run(input_documents=docs, question=query) 
    return answer 

def main():
    load_dotenv() 

    llm = AzureChatOpenAI(deployment_name="gpt-4") 
    pdf_path = "stories.pdf" 
    
    vectorstore = create_vector_store(pdf_path) 
    
    vector_tool = Tool( name="VectorDBTool",
                       func=lambda q: vector_search(q, vectorstore, llm),
                       description="Use this tool for questions related to the PDF document content. It contains kids stories" )
    
    web_search_tool = Tool( name="WebSearchTool", 
                           func=DuckDuckGoSearchResults().run, 
                           description="Use this tool for web searches using DuckDuckGo." )
     
    tools = [vector_tool,web_search_tool,YahooFinanceNewsTool()]

    memory = ConversationBufferMemory(memory_key="chat_history") 
    
    master_agent = initialize_agent( tools, 
                                    llm, 
                                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                    verbose=True, 
                                    memory=memory)
    
    print("Agentic AI is running. Type 'exit' to quit.") 
    
    while True: 
        user_input = input("You: ") 
        if user_input.lower() in ["exit", "quit"]:
            break 
        elif user_input.lower() == "cls":
            os.system("cls")
            continue
            
        response = master_agent.run(user_input) 
        print("Agent:", response) 
        
if __name__ == "__main__":
    main()