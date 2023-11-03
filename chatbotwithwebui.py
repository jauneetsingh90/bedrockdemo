from langchain.chains import RetrievalQA
from langchain.llms import Bedrock
from langchain.vectorstores import Cassandra
import boto3
import streamlit as st
import os
from astra_connection import get_astra
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms.bedrock import Bedrock
from astra_connection import get_astra
from langchain.embeddings import BedrockEmbeddings
from embeddings_generator import generate_embeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import Bedrock
from langchain.vectorstores import Cassandra

session, keyspace = get_astra()
model_id = "anthropic.claude-v2"

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by Bedrock")
st.header("Welcome to certPrep You can speak to this bot")

# Initialize the `messages` key in the `st.session_state` dictionary if it does not exist.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1', 
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
)

BEDROCK_MODEL = "amazon.titan-embed-text-v1"

model_kwargs =  { 
    "max_tokens_to_sample": 8191,
    "temperature": 0.5,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": ["\n\nHuman"],
}
prompt_template = """
Human: Use the following pieces of context to provide a concise answer to the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
<context>
{context}
</context
Question: {question}
Assistant:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"])

llm = Bedrock(
    client=bedrock,
    model_id=model_id,
    model_kwargs=model_kwargs
)
embeddings = BedrockEmbeddings(model_id=BEDROCK_MODEL, client=bedrock)
vectorstore = Cassandra(
        embedding=embeddings,
        session=session,
        keyspace=keyspace,
        table_name="awsguide1",
    )
# Sample URLs for user and assistant avatars
assistant_avatar_url = "/Users/jauneet.singh/Downloads/awschat/images/ai-icon.png"
user_avatar_url = "/Users/jauneet.singh/Downloads/awschat/images/user-icon.png"
if prompt := st.chat_input():
    try:
        # Append the user's message to the `messages` list.
        st.session_state["messages"].append({"role": "user", "content": prompt})

        # Display the user's message with the user avatar.
        st.image(user_avatar_url, caption="User", width=100)
        st.write("User:", prompt)

        # Create a query for the chatbot.
        query = (f"\n\nHuman:{prompt}\n\nAssistant:")

        # Call the chatbot.
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
        response = qa_chain({"query": query})

        # Get the chatbot's response.
        answer = response['result']
        
        # Append the chatbot's response to the `messages` list.
        st.session_state["messages"].append({"role": "assistant", "content": answer})

        # Display the assistant's message with the assistant avatar.
        st.image(assistant_avatar_url, caption="Assistant", width=100)
        st.write("Assistant:", answer)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display all questions and responses
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.image(user_avatar_url, caption="User", width=100)
        st.write("User:", message["content"])
    elif message["role"] == "assistant":
        st.image(assistant_avatar_url, caption="Assistant", width=100)
        st.write("Assistant:", message["content"])
