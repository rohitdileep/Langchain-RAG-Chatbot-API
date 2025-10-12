from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage , AIMessage

from langchain.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever , create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
import os 
from langchain_chroma import Chroma

##Loading API keys ##
load_dotenv()

groq_api_key = os.environ["groq_api_key"]

##Prompts and Chains##
contextualize_q_system_prompt = ("Given a user chat history and a latest question"
                                 "Which might reference to the chat history"
                                 "Formulate a standalone question that is clear"
                                 "Without the chat history do not answer the question"
                                 "Just reformulate it if needed, otherwise return the question as is")


contextualize_prompt =  ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    (MessagesPlaceholder(variable_name="chat_history")),
    ("human", "{input}"), ])

##LLM 
llm  = ChatGroq(model="llama-3.3-70b-versatile", temperature=0 , api_key = groq_api_key)

## History aware Retriever
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vectorstore = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

# Get retriever
retriever = vectorstore.as_retriever()



history_aware_retriever = create_history_aware_retriever(
    retriever=retriever,
    prompt=contextualize_prompt,
    llm=llm )


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that helps people find information."),
    ("system", "Here are some relevant documents:\n{context}"), 
    ("human", "{input}")
])


document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
qa_chain = create_retrieval_chain(history_aware_retriever, document_chain )

chat_history = []
def get_response(chat_history, question):
    try:
        result = qa_chain.invoke({'input': question, 'chat_history': chat_history})
        print(f'Question : {question}')
        print(f'Testing Retriever {retriever.invoke("when was GreenGrow founded?")}' )
        answer = result['answer']
        print(f"[DEBUG] Raw chain result: {result}")
    except Exception as e:
        print(f"Error during QA chain invocation: {e}")
       
    chat_history.extend([
        HumanMessage(content=question),
        AIMessage(content=answer)
    ])
    return answer, chat_history
