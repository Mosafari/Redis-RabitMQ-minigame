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


