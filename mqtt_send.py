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

@rpc.register
def IF_MQTT_SEND(params):
    deviceId = params['deviceId']
    cmd = str(params['cmd'])
    sendChannel.basic_publish(exchange='amq.topic', routing_key='.%s'%deviceId, body=cmd)

rpc.loop()
