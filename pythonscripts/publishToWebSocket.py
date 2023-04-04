# Instructions :
#    pip install websocket-client
# Log into your Vantiq server and create an access token. 
# Set the correct URL, Token and Topic name values below

import websocket
import json
import time

try:
    import thread
except ImportError:
    import _thread as thread
import time

URL = "wss://internal.vantiq.com/api/v1/wsock/websocket"
Token = "<your-vantiq-token>"
Topic = "/devicedata"
Payload1 = {"requestId": "Publish123"}
Payload2 =  {"datakey": "datavalue"}

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):   
    ws.send(json.dumps({ "op": "validate", "resourceName": "system.credentials", "object": Token}))
    time.sleep(5)
    on_query(ws)
    pub_msg(ws)

def on_query(ws):
    print("sending query request")
    ws.send(json.dumps({"op": "select", "resourceName": "patients", "parameters": { } }))

def pub_msg(ws):
    print("publishing message to topic")
    ws.send(json.dumps({ "op": "publish", "resourceName": "topics", "resourceId":Topic, "object": Payload1}))
    time.sleep(5)
    ws.send(json.dumps({ "op": "publish", "resourceName": "topics", "resourceId":Topic, "object": Payload2}))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(URL,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
