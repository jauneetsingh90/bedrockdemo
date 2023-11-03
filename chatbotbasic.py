import json
import boto3
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
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

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1', 
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
)
BEDROCK_MODEL = "amazon.titan-embed-text-v1"

def claude_prompt_format(prompt: str) -> str:
    # Add headers to start and end of prompt
    return "\n\nHuman: " + prompt + "\n\nAssistant:"

def call_claude(prompt):
    prompt_config = {
        "prompt": claude_prompt_format(prompt),
        "max_tokens_to_sample": 4096,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 0.5,
        "stop_sequences": [],
    }

    body = json.dumps(prompt_config)

    modelId = "anthropic.claude-v2"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    results = response_body.get("completion")
    return results

def rag_setup(query):  
    embeddings = BedrockEmbeddings(model_id=BEDROCK_MODEL, client=bedrock)
    vectorstore = Cassandra(
        embedding=embeddings,
        session=session,
        keyspace=keyspace,
        table_name="awsguide1",
    )

    docs = vectorstore.similarity_search(query)
    context = ""

    for doc in docs:
        context += doc.page_content

    prompt = f"""Use the following pieces of context to answer the question at the end.

    {context}

    Question: {query}
    Answer:"""

    return call_claude(prompt)


query = "What is RDS instances?"
print(query)
print(rag_setup(query))