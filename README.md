# bedrockdemo
Demo chatbot with the bedrock.
The purpose of this demo is to build a chatbot using AstraDB and Amazon bedrock as LLM.

We need to export the AWS credentials like the access key and secret key as below for the demo.
  export AWS_ACCESS_KEY_ID='accesskey'
  export AWS_SECRET_ACCESS_KEY='secretkey'

  or create the env file and load the keys through same 
  vi .env  
  # Add all variable keys 
export AWS_ACCESS_KEY_ID='accesskey'
export AWS_SECRET_ACCESS_KEY='secretkey'
export SECURE_CONNECT_BUNDLE_PATH = "<Bundle Location>"
export ASTRA_CLIENT_ID = 'clientid'
export ASTRA_CLIENT_SECRET = 'secret key'
export ASTRA_KEYSPACE_NAME = 'keyspacename'
export ASTRA_APPLICATION_TOKEN = token



