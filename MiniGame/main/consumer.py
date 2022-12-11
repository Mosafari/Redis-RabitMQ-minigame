# impord module
import pika,os,sys


# rabitMQ consumer
#defining callback functions responding to corresponding queue callbacks
def callbackFunctionForPersonality(ch,method,properties,body):
    score[body.decode('utf-8')[:-13]]=int(body.decode('utf-8')[-1])
    print('Result Of Personality Chat : ', body.decode('utf-8'))
    
def callbackFunctionForPassion(ch,method,properties,body):
    score[body.decode('utf-8')[:-9]]+=int(body.decode('utf-8')[-1])
    print('Result Of Passion Chat : ', body.decode('utf-8'))
    
def callbackFunctionForHobbie(ch,method,properties,body):
    score[body.decode('utf-8')[:-8]]+=int(body.decode('utf-8')[-1])
    print('Result Of Hobbie Chat : ', body.decode('utf-8'))
    
def WhatHappened(WH):
    # Attaching consumer callback functions to respective queues that we wrote above
    # issue3 : it goes to infinite loop to get message
    # try:
    global channel
    credentials =  pika.PlainCredentials('me', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare('dates', durable=True, exchange_type='topic')
    if WH == "Personality":
        channel.basic_consume(queue='Personality', on_message_callback=callbackFunctionForPersonality, auto_ack=True)
    elif WH == "Passion":
        channel.basic_consume(queue='Passion', on_message_callback=callbackFunctionForPassion, auto_ack=True)
    elif WH == "Hobbie":
        channel.basic_consume(queue='Hobbie', on_message_callback=callbackFunctionForHobbie, auto_ack=True)  
    channel.start_consuming()
    # except KeyboardInterrupt:
    #     pass
    #this will be command for starting the consumer session
    
if __name__ == '__main__':
    score = {}
    Dates = ['Personality', 'Passion', 'Hobbie']
    player = ["PL1", "PL2"]
    for i in Dates:
        for _ in player:
            try:
                WhatHappened(i)
            except KeyboardInterrupt:
                continue
        print(score)
        print(i," done")
        channel.close()
    # send result to producer
    if sum(list(score.values())) > 3 and (list(score.values())[0]> 1):
        final = "pass"
    else:
        final = "fail"
    credentials =  pika.PlainCredentials('me', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare('dates', durable=True, exchange_type='topic')
    channel.queue_declare(queue= 'finalresult')
    channel.queue_bind(exchange='dates', queue='finalresult', routing_key='finalresult')
    channel.basic_publish(exchange='dates', routing_key='finalresult', body= final)
    channel.close()
    print("Final Result : ",final)
