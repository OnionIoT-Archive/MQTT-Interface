import amqp_rpc as rpc
import pika
import time

MQ_USER = 'onionCore'
MQ_PASS = 'p'
MQ_HOST = 'mqtt.onion.io'

credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
parameters = pika.ConnectionParameters(credentials=credentials, host=MQ_HOST, virtual_host='/')

sendConnection = pika.BlockingConnection(parameters)
sendChannel = sendConnection.channel()

#@rpc.register
#def IF_MQTT_SEND(params):
#    deviceId = params['deviceId']
#    cmd = str(params['cmd'])
#    sendChannel.basic_publish(exchange='amq.topic', routing_key='.%s'%deviceId, body=cmd)

def mqttRegFunction(params):
    payload = {}
    payload['path'] = params['path']
    payload['verb'] = params['verb']
    payload['deviceId'] = params['deviceId']
    payload['functionId'] = params['functionId']
    if params['verb'].upper() == "POST":
        payload['postParams'] = params['postParams']
    else:
        payload['postParams'] = []
    rpc.call('DB_ADD_PROCEDURE', payload)

def onResponse(ch, method, props, body):
    data = body.split(';')
    deviceId = data[0]
    verb = data[1]
    path = ''
    functionId = 0
    postParams = []
    if len(data) > 2:
        path = data[2]

    if len(data) > 3:
        functionId = data[3]

    if len(data) > 4:
        postParams = data[4].split(',')

    if verb == 'CONNECTED':
        rpc.call('DB_REMOVE_PROCEDURE',{'deviceId': deviceId})
        rpc.call('DB_ADD_HISTORY', {
            'deviceId': deviceId,
            'action': "power on"
            })
    elif verb == 'GET' or verb == "POST":
        payload = {}
        payload['path'] = path
        payload['verb'] = verb
        payload['deviceId'] = deviceId
        payload['functionId'] = functionId
        if verb.upper() == "POST":
            payload['postParams'] = postParams
        else:
            payload['postParams'] = []
        rpc.call('DB_ADD_PROCEDURE', payload)
    elif verb == 'UPDATE': 
        payload = {}
        payload['path'] = path
        payload['deviceId'] = deviceId
        payload['value'] = functionId
        rpc.call('DB_ADD_STATE', payload)


    print data

def startMqttListener():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    result = channel.queue_declare(exclusive=True)
    queue = result.method.queue
    channel.queue_bind(exchange='amq.topic', queue=queue, routing_key='.register')
    channel.queue_bind(exchange='amq.topic', queue=queue, routing_key='.update')
    channel.basic_consume(onResponse, queue=queue, no_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    #rpc.loop()
    startMqttListener()



