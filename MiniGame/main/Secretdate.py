# importing modules
import redis
import pika

# connect to redis
def Red(mode, chat, datenum, name):
    r = redis.Redis()
    if mode == "set":
        r.mset({name+datenum:chat})
    elif mode == "get":
        return r.mget(name+datenum).decode('utf-8')


# rabitMQ consumer
#defining callback functions responding to corresponding queue callbacks
def callbackFunctionForDate1(ch,method,properties,body):
    print('Result Of Date1: ', body)
    
def callbackFunctionForDate2(ch,method,properties,body):
    print('Result Of Date2: ', body)
    
def callbackFunctionForDate3(ch,method,properties,body):
    print('Result Of Date3: ', body)
    
def callbackFunctionForResult(ch,method,properties,body):
    print('Final Result: ', body)
    
def WhatHappened(WH):
    #Attaching consumer callback functions to respective queues that we wrote above
    if WH == "date1":
        channel.basic_consume(queue='date1', on_message_callback=callbackFunctionForDate1, auto_ack=True)
    elif WH == "date2":
        channel.basic_consume(queue='date2', on_message_callback=callbackFunctionForDate2, auto_ack=True)
    elif WH == "date3":
        channel.basic_consume(queue='date3', on_message_callback=callbackFunctionForDate3, auto_ack=True)
    elif WH == "finalresult":
        channel.basic_consume(queue='finalresult', on_message_callback=callbackFunctionForResult, auto_ack=True)
    
    #this will be command for starting the consumer session
    channel.start_consuming()

# rabitMQ producer
def producer(queue, result, final, datenum, name, close=False):
    if queue == "date1":
        channel.basic_publish(exchange='dates', routing_key='Personality', body= {name+datenum:result})
        if close :
            channel.close()
    elif queue == "date2":
        channel.basic_publish(exchange='dates', routing_key='Passion', body= {name+datenum:result})
        if close :
            channel.close()
    elif queue == "date3":
        channel.basic_publish(exchange='dates', routing_key='Hobbie', body= {name+datenum:result})
        if close :
            channel.close()
    elif queue == "finalresult":
        channel.basic_publish(exchange='dates', routing_key='finalresult', body= final)
        if close :
            channel.close()
    


# main function


