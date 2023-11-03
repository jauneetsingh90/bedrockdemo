#Importing the libraries
import configparser
import boto3
from langchain.embeddings import BedrockEmbeddings
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Cassandra
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms.bedrock import Bedrock
from astra_connection import get_astra
import os

BEDROCK_MODEL = "amazon.titan-embed-text-v1"


bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1', 
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
)

pdf_loaders = []

    # List objects in the S3 bucket
s3_client = boto3.client(
    service_name='s3',
    region_name='us-west-2', 
    aws_access_key_id= os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key= os.environ.get("AWS_SECRET_ACCESS_KEY")
)

    # Get a list of all PDF files in the S3 folder
S3_BUCKET = 'glue-test-jaubeet'
S3_FOLDER= 'files2/'
LOCAL_FOLDER= '/Users/jauneet.singh/Downloads/pdf1/'
pdf_files = []
try:
    objects = s3_client.list_objects(Bucket=S3_BUCKET, Prefix=S3_FOLDER)
    
    for obj in objects.get("Contents", []):
        if obj['Key'].endswith('.pdf'):
            pdf_files.append(obj["Key"])

except Exception as e:
    print(f"An error occurred while listing objects: {str(e)}")

# Download and save PDF files locally
for pdf_file in pdf_files:
    local_path = os.path.join(LOCAL_FOLDER, os.path.basename(pdf_file))

    try:
        with open(local_path, 'wb') as local_file:
            s3_client.download_fileobj(S3_BUCKET, pdf_file, local_file)

        print(f"Downloaded '{pdf_file}' to '{local_path}'")

    except Exception as e:
        print(f"An error occurred while downloading '{pdf_file}': {str(e)}")

print("PDF files downloaded and saved locally.")



FILE_SUFFIX = ".pdf"

def generate_embeddings():
    embeddings = BedrockEmbeddings(model_id=BEDROCK_MODEL, client=bedrock)
    #
    pdf_loaders = [
        PyPDFLoader(pdf_name)
        for pdf_name in (
            f for f in (
                os.path.join(LOCAL_FOLDER, f2)
                for f2 in os.listdir(LOCAL_FOLDER)
            )
            if os.path.isfile(f)
            if f[-len(FILE_SUFFIX):] == FILE_SUFFIX
        )
    ]

    # set up the vector store
    session, keyspace = get_astra()
    vectorstore = Cassandra(
        embedding=embeddings,
        session=session,
        keyspace=keyspace,
        table_name="awsguide2",
    )

    # strip and load the docs
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )
    documents = [
        doc
        for loader in pdf_loaders
        for doc in loader.load_and_split(text_splitter=text_splitter)
    ]
    #
    texts, metadatas = zip(*((doc.page_content, doc.metadata) for doc in documents))
    vectorstore.add_texts(texts=texts, metadatas=metadatas,batch_size=30)
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    return vectorstore, index
print("Uploaded")

if __name__ == "__main__":
    vectorstore = generate_embeddings()