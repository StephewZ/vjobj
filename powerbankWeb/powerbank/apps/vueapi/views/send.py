#!/usr/bin/env python
#coding=utf8
import pika

MQ_IP = 'test1.amqp.gzncloud.com'
MQ_PORT = 5672
MQ_ID = 'ssdd01'
MQ_PW = '*ssdd_password#'
MQ_exchange = 'to_ssdd_server'

credentials = pika.PlainCredentials(MQ_ID, MQ_PW)

connection = pika.BlockingConnection(pika.ConnectionParameters(
               MQ_IP, MQ_PORT, '/', credentials))
channel = connection.channel()
 
channel.basic_publish(exchange=MQ_exchange, routing_key='operation:1700123456', body='1100')
print (" [x] Sent 'Hello World!'")
connection.close()