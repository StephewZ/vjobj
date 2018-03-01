#!/usr/bin/env python
#coding=utf8
import pika

MQ_IP = 'test1.amqp.gzncloud.com'
MQ_PORT = 5672
MQ_ID = 'ssdd01'
MQ_PW = '*ssdd_password#'
MQ_exchange = 'to_ssdd_server'

def sentMQ(key, body):
	credentials = pika.PlainCredentials(MQ_ID, MQ_PW)

	connection = pika.BlockingConnection(pika.ConnectionParameters(
	               MQ_IP, MQ_PORT, '/', credentials))
	channel = connection.channel()
	 
	channel.basic_publish(exchange=MQ_exchange, routing_key=key, body=body)
	print (" [x] Sent: " + " routing_key=" + key + " body=" + body)
	connection.close()
msga = 'operation:' + '180200001'
msgb = [1,1,1,0,0,0,0,0]
msgb = str(bytes(msgb), encoding='utf-8')
sentMQ(msga, msgb)