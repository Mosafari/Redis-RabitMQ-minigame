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
def callbackFunctionForPersonality(ch,method,properties,body):
    print('Result Of Personality Chat : ', body)
    
def callbackFunctionForPassion(ch,method,properties,body):
    print('Result Of Passion Chat : ', body)
    
def callbackFunctionForHobbie(ch,method,properties,body):
    print('Result Of Hobbie Chat : ', body)
    
def callbackFunctionForResult(ch,method,properties,body):
    print('Final Result : ', body)
    
def WhatHappened(WH):
    #Attaching consumer callback functions to respective queues that we wrote above
    if WH == "Personality":
        channel.basic_consume(queue='Personality', on_message_callback=callbackFunctionForPersonality, auto_ack=True)
    elif WH == "Passion":
        channel.basic_consume(queue='Passion', on_message_callback=callbackFunctionForPassion, auto_ack=True)
    elif WH == "Hobbie":
        channel.basic_consume(queue='Hobbie', on_message_callback=callbackFunctionForHobbie, auto_ack=True)
    elif WH == "finalresult":
        channel.basic_consume(queue='finalresult', on_message_callback=callbackFunctionForResult, auto_ack=True)
    
    #this will be command for starting the consumer session
    channel.start_consuming()

# rabitMQ producer
def producer(queue, result, datenum, name, close=False, final=None):
    # issue1 : body just accept str
    # issue2 : connection closed
    if queue == "Personality":
        channel.basic_publish(exchange='dates', routing_key='Personality', body= f'{name}{datenum}:{result}')
    elif queue == "Passion":
        channel.basic_publish(exchange='dates', routing_key='Passion', body= f'{name}{datenum}:{result}')
    elif queue == "Hobbie":
        channel.basic_publish(exchange='dates', routing_key='Hobbie', body= f'{name}{datenum}:{result}')
    elif queue == "finalresult":
        channel.basic_publish(exchange='dates', routing_key='finalresult', body= final)
        if close :
            channel.close()
    


# main function
def main():
    player = ["PL1", "PL2"]
    PLinfo = {}
    for i in player:
        nickname = input("Enter your nickname : ")
        number = input("Enter your number : ")
        PLinfo[nickname] = number
    r = redis.Redis()
    r.mset(PLinfo)
    Dates = ['Personality', 'Passion', 'Hobbie']
    for d in Dates :
        print("Talk about ", d, " :")
        for p in PLinfo.keys():
            # one line chat
            chat = input(p+" : ")
            Red("set", chat, d, p)
        for pn in PLinfo.keys():
            # in next Update : this will send each message to another player then go to get score
            # results of the date
            result = input(pn+" : Do You Like Her/Him ? (1 -> Yes, 0 ->No) ")
            producer(d, result, d, pn)
            if pn == list(PLinfo)[-1]:
                producer(d, result, d, pn, close=True)
    
    print("End Of Chat! ")

credentials =  pika.PlainCredentials('me', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()
channel.exchange_declare('dates', durable=True, exchange_type='topic')
channel.queue_declare(queue= 'date1')
channel.queue_bind(exchange='dates', queue='date1', routing_key='Personality')
channel.queue_declare(queue= 'date2')
channel.queue_bind(exchange='dates', queue='date2', routing_key='Passion')
channel.queue_declare(queue= 'date3')
channel.queue_bind(exchange='dates', queue='date3', routing_key='Hobbie')
channel.queue_declare(queue= 'finalresult')
channel.queue_bind(exchange='dates', queue='finalresult', routing_key='finalresult')
main()
    
    
    
