import json
import requests
from requests.auth import HTTPBasicAuth
import os
import base64
import random

#Set env variables, these should be set in the docker-compose.yml configuration, else set fallback defaults
nodename = os.getenv('NODENAME') if os.getenv('NODENAME') else 'EdgeNode' + str(random.randrange(1000, 9000, 13))
edgeNodeProperties = os.getenv('NODEPROPERTIES') if os.getenv('NODEPROPERTIES') else {"type":"edge"}
cloudToken = os.getenv('CLOUDTOKEN') if os.getenv('CLOUDTOKEN') else '<add a default token here>'
cloudNodeName = os.getenv('CLOUDNODENAME') if os.getenv('CLOUDNODENAME') else 'Cloud_Master'
cloudNodeProperties = os.getenv('CLOUDPROPERTIES') if os.getenv('CLOUDPROPERTIES') else {"type":"cloud"}

def edgeCommands():
    #Base64 encoded login for basic auth
    user='<default vantiq login>'
    password='<default vantiq password>'

    #Generate Auth token    
    getToken = requests.get('http://localhost:8080/authenticate', auth=HTTPBasicAuth(user,password))
    json_data = getToken.json()
    accessToken = json_data['accessToken']
    
    #Insert the cloud node using the virtual websocket 
    uri = 'wss://dev.vantiq.com?vqs=' + nodename
    headers = {'Content-Type':'application/json'}
    query = {'token':accessToken}
    body = {'name':'CloudAI_Master', 'credentialType':'token', 'uri': uri, 'accessToken':cloudToken, 'deliveryMode':'bestEffort', 'ars_properties':cloudNodeProperties}
    response = requests.post("http://localhost:8080/api/v1/resources/nodes", headers=headers, params=query, data=json.dumps(body))    

    #Generate a long lived token for the Cloud configuration needed to access the Edge node
    edgeToken = getLongLivedToken(accessToken)        
    cloudCommands(edgeToken)
    
    #Force the Test Connection activity to open the web socket. 
    forceTestConnection(accessToken)
    

def cloudCommands(edgeToken):    
    #Insert the Edge node definition into the Cloud system using the VQS connection URL
    query = {'token':cloudToken} 
    body = {'nodename':nodename, 'token':edgeToken, 'nodeproperties':edgeNodeProperties}
    headers = {'Content-Type':'application/json'}    
    response = requests.post("http://internal.vantiq.com/api/v1/resources/procedures/edge_bootstrap", params=query, data=json.dumps(body), headers=headers )

def getLongLivedToken(accessToken):
    query = {'token':accessToken}
    body = { 'profiles': ['system.admin'], 'name': 'LongLivedVQS_Token' + str(random.randrange(1000, 9000, 13)), 'tokenTimeout': 3155695200 }
    headers = {'Content-Type':'application/json'}   
    response = requests.post('http://localhost:8080/api/v1/resources/tokens', params=query, data=json.dumps(body), headers=headers)
    json_data = response.json()
    longLivedToken = json_data['accessToken']
    return longLivedToken
    
def forceTestConnection(accessToken):    
    query = {'token':accessToken}
    headers = {'Content-Type':'application/json'}
    body = {}
    response = requests.post('http://localhost:8080/api/v1/resources/procedures/Utils.getNamespaceAndProfiles?processedBy={\"remoteNodes\":{\"name\":\"CloudAI_Master\"}}', params=query, headers=headers, data=json.dumps(body))

edgeCommands()




