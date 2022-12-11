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


# move consumer to seperate file

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

# add  producer for result in consumer 

# main function
# del numbers in py file (we can get the numbers from redis)
def main():
    player = ["PL1", "PL2"]
    PLinfo = []
    r = redis.Redis()
    for i in player:
        nickname = input("Enter your nickname : ")
        number = input("Enter your number : ")
        PLinfo.append(nickname)
        r.mset({nickname: number})
    Dates = ['Personality', 'Passion', 'Hobbie']
    for d in Dates :
        print("Talk about ", d, " :")
        for p in PLinfo:
            # one line chat
            chat = input(p+" : ")
            Red("set", chat, d, p)
        for pn in PLinfo:
            # in next Update : this will send each message to another player then go to get score
            # results of the date
            result = input(pn+" : Do You Like Her/Him ? (1 -> Yes, 0 ->No) ")
            producer(d, result, d, pn)
    channel.close()
    
    print("End Of Chat! ")
    # for i in Dates:
    #     for j in player:
    #         WhatHappened(i)
    

credentials =  pika.PlainCredentials('me', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()
channel.exchange_declare('dates', durable=True, exchange_type='topic')
channel.queue_declare(queue= 'Personality')
channel.queue_bind(exchange='dates', queue='Personality', routing_key='Personality')
channel.queue_declare(queue= 'Passion')
channel.queue_bind(exchange='dates', queue='Passion', routing_key='Passion')
channel.queue_declare(queue= 'Hobbie')
channel.queue_bind(exchange='dates', queue='Hobbie', routing_key='Hobbie')

main()
    
    
    
