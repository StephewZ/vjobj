#!/usr/bin/env python
#coding=utf8
import pika

MQ_IP = 'test1.amqp.gzncloud.com'
MQ_PORT = 5672
MQ_ID = 'ssdd01'
MQ_PW = '*ssdd_password#'
MQ_exchange = 'from_ssdd_server'

credentials = pika.PlainCredentials(MQ_ID, MQ_PW)

connection = pika.BlockingConnection(pika.ConnectionParameters(
               MQ_IP, MQ_PORT, '/', credentials))
channel = connection.channel()
 
#定义交换机
 
#随机生成队列，并绑定到交换机上
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='from_ssdd_server', queue=queue_name)
 
def callback(ch, method, properties, body):
    print (body)
    print(method.routing_key)
 
channel.basic_consume(callback, queue=queue_name, no_ack=True)
 
print (' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()