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
orgName = os.getenv('ORGNAME') if os.getenv('ORGNAME') else 'AIEdge'
orgRoot = os.getenv('ORGROOT') if os.getenv('ORGROOT') else 'edge_ai_root'
appNamespaceName = os.getenv('APPNAMESPACE') if os.getenv('APPNAMESPACE') else 'edge_ai_app'
vantiqServerURL = os.getenv('VANTIQSERVER') if os.getenv('VANTIQSERVER') else 'internal.vantiq.com'

def createEdgeAuthToken():
    #Base64 encoded login for basic auth
    user=<default username>
    password=<default password>

    #Generate an edge auth token using default system credentials
    print('Creating local auth token')
    getToken = requests.get('http://localhost:8080/authenticate', auth=HTTPBasicAuth(user,password))
    print(getToken.status_code)
    json_data = getToken.json()
    accessToken = json_data['accessToken']
    return accessToken
    
def insertCloudNodeOnEdgeSite(accessToken):
    #Insert the cloud node 
    print('Creating cloud node definition at the edge')
    uri = 'wss://' + vantiqServerURL + '?vqs=' + nodeName
    headers = {'Content-Type':'application/json', 'X-Target-Namespace':appNamespaceName}
    query = {'token':accessToken}
    body = {'name':cloudNodeName, 'credentialType':'token', 'uri': uri, 'accessToken':cloudToken, 'deliveryMode':'bestEffort', 'ars_properties':cloudNodeProperties}
    response = requests.post('http://localhost:8080/api/v1/resources/nodes', headers=headers, params=query, data=json.dumps(body))    
    print(response.status_code)
    
def insertEdgeNodeOnCloudSite(edgeToken):
    #Insert the Edge node definition into the Cloud system using the VQS connection URL
    print('Creating edge node definition at the cloud')
    uri = 'vqs://' + nodeName
    query = {'token':cloudToken} 
    body = {'name':nodeName, 'credentialType':'token', 'uri': uri, 'accessToken':edgeToken, 'deliveryMode':'bestEffort', 'ars_properties':edgeNodeProperties}
    headers = {'Content-Type':'application/json'}    
    response = requests.post('https://' + vantiqServerURL + '/api/v1/resources/nodes', params=query, data=json.dumps(body), headers=headers )
    print(response.status_code)

def getEdgeNodeLongLivedToken(accessToken):
    #Create long lived edge token
    print('Creating LongLived Access Token')
    query = {'token':accessToken}
    body = { 'profiles': [appNamespaceName + '.admin', appNamespaceName + '.admin__system'], 'name': 'LongLivedVQS_Token' + str(random.randrange(1000, 9000, 13)), 'tokenTimeout': 3155695200 }
    headers = {'Content-Type':'application/json', 'X-Target-Namespace':appNamespaceName}   
    response = requests.post('http://localhost:8080/api/v1/resources/tokens', params=query, data=json.dumps(body), headers=headers)
    print(response.status_code)
    json_data = response.json()
    longLivedToken = json_data['accessToken']
    return longLivedToken
    
def forceTestConnection(accessToken):
    #Opening websocket
    print('Initialize wss connection')
    query = {'token':accessToken}
    headers = {'Content-Type':'application/json', 'X-Target-Namespace':appNamespaceName}
    body = {}
    response = requests.post('http://localhost:8080/api/v1/resources/procedures/Utils.getNamespaceAndProfiles?processedBy={\"remoteNodes\":{\"name\":\"' + cloudNodeName  + '\"}}', params=query, headers=headers, data=json.dumps(body))                              
    print(response.status_code)

#Create Organization and Root Namespace
def createOrgnizationRoot(accessToken):
    print('Creating Organization')
    query = {'token':accessToken}
    headers = {'Content-Type':'application/json' }   
    body = {'namespace':orgRoot,'organization':{'name':orgName,'description':orgName,'isIsolated':False,'vCPU':0,'perServerMemory':0,'monitoringConfig':{'enable':True},'products':{'Pronto':{'enabled':True,'maxEventCatalogs':1},'Modelo':{'enabled':True},'IDE':{'disableBadging':False}}},'organizationRef':None,'encryptionKey':None,'isOrgNamespace':False,'adminUserAuthZ':'current'}
    response = requests.post('http://localhost:8080/api/v1/resources/namespaces', params=query, headers=headers, data=json.dumps(body))
    print(response.status_code)

#Create Application Namespace
def createApplicationNamespace(accessToken):
    print('Creating Application Namespace')
    query = {'token':accessToken}
    headers = {'Content-Type':'application/json', 'X-Target-Namespace':orgRoot }   
    body = {'namespace': appNamespaceName ,'organization':'','organizationRef':None,'encryptionKey':None,'isOrgNamespace':False,'adminUserAuthZ':'current','systemProfile':'system.federatedAdmin'} 
    response = requests.post('http://localhost:8080/api/v1/resources/namespaces', params=query, headers=headers, data=json.dumps(body))    
    print(response.status_code)

#Deploy the chooch application to the edge system
def deployChoochEdgeRequired():
    print('Deploy Chooch app part 1')
    query = {'token':cloudToken} 
    headers = {'Content-Type':'application/json'}
    body = {"configName":"ChoochEdgeRequired","globalId":str(uuid.uuid4()),"errorsOnly":False}
    response = requests.post('https://' + vantiqServerURL + '/api/v1/resources/procedures/Deployment.deployPartitions', params=query, headers=headers, data=json.dumps(body))  
    print(response.status_code)

def deployFallDetection():
    print('Deploy Chooch app part 2')
    query = {'token':cloudToken} 
    headers = {'Content-Type':'application/json'}
    body = {"configName":"FallDetection","globalId":str(uuid.uuid4()),"errorsOnly":False}
    response = requests.post('https://' + vantiqServerURL + '/api/v1/resources/procedures/Deployment.deployPartitions', params=query, headers=headers, data=json.dumps(body)) 
    print(response.status_code)

def deployFireDetection():
    print('Deploy Chooch app part 3')
    query = {'token':cloudToken} 
    headers = {'Content-Type':'application/json'}
    body = {"configName":"FireDetection","globalId":str(uuid.uuid4()),"errorsOnly":False}
    response = requests.post('https://' + vantiqServerURL + '/api/v1/resources/procedures/Deployment.deployPartitions', params=query, headers=headers, data=json.dumps(body)) 
    print(response.status_code)

def deployPPEDetection():
    print('Deploy Chooch app part 4')
    query = {'token':cloudToken} 
    headers = {'Content-Type':'application/json'}
    body = {"configName":"PPEDetection","globalId":str(uuid.uuid4()),"errorsOnly":False}
    response = requests.post('https://' + vantiqServerURL + '/api/v1/resources/procedures/Deployment.deployPartitions', params=query, headers=headers, data=json.dumps(body)) 
    print(response.status_code)

def runBootstrapActivities():
    #Get a local system root login token
    accessToken = createEdgeAuthToken()
    print(accessToken)

    #Create ORG Root
    createOrgnizationRoot(accessToken)

    #Create App namespace
    createApplicationNamespace(accessToken)

    #Insert cloud node entry on Edge site
    insertCloudNodeOnEdgeSite(accessToken)

    #Create a new LongLived access token needed for edge node entry
    edgeToken = getEdgeNodeLongLivedToken(accessToken)
    print(edgeToken)

    #Insert the edge node setup in the cloud system
    insertEdgeNodeOnCloudSite(edgeToken)
    
    #Use test connection to initizie the websocket connection
    forceTestConnection(accessToken)

    #Deploy Chooch applications to edge
    deployChoochEdgeRequired()
    deployFallDetection()
    deployFireDetection()
    deployPPEDetection()

runBootstrapActivities()




