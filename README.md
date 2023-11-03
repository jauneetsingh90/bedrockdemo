# bedrockdemo
Demo chatbot with the bedrock.
The purpose of this demo is to build a chatbot using AstraDB and Amazon bedrock as LLM.

# Create the env file and add the variable/secrets as below
export AWS_ACCESS_KEY_ID='accesskey'</br>
export AWS_SECRET_ACCESS_KEY='secretkey'</br>
export SECURE_CONNECT_BUNDLE_PATH="<Bundle Location>"</br>
export ASTRA_CLIENT_ID='clientid'</br>
export ASTRA_CLIENT_SECRET='secret key'</br>
export ASTRA_KEYSPACE_NAME='keyspace name'</br>
export ASTRA_APPLICATION_TOKEN='token'</br>

Run the command as below </br>
source .env

# Now, to generate the embedding, run the command below
python3 embeddings_generator.py </br>

It will generate the embeddings for the files in the s3 folder. </br>

# Now to run the chatbot with WebUI, run the command below
 
streamlit run chatbotwithwebui.py






