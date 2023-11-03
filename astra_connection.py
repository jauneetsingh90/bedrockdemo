# astra_connection.py
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

def get_astra():
    keyspace = 'vectordb'
    table = 'embeddings'
    cloud_config = {'secure_connect_bundle': '/Users/jauneet.singh/Downloads/secure-connect-mydb.zip'}
    
    # Load the credentials from a hidden file
    #with open('.credentials', 'r') as file:
        #username, password = file.read().strip().split(':')

    auth_provider = PlainTextAuthProvider(os.environ.get("ASTRA_CLIENT_ID"), os.environ.get("ASTRA_CLIENT_SECRET"))
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect(keyspace)
    
    return session, keyspace
