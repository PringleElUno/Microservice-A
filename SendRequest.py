import zmq
import json


# Sets up our ZeroMQ 
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:7979") # remember we want to use the beautful 7979 port


# this will contain ten dictionaries inside of a list that can be sent
bank_name = "SampleArticleBank"
article_bank = [
    {"Article": 1, "title": "The supressor"},
    {"Article": 2, "title": "The 8 ways of fungshi"},
    {"Article": 3, "title": "How to fly a dragon"},
    {"Article": 4, "title": "Cooking smarter and cleaner"},
    {"Article": 5, "title": "How can we save more money as Americans"},
    {"Article": 6, "title": "To be or not to be, alphabet soup and how good is it really?"},
    {"Article": 7, "title": "The many names we keep for our kids"},
    {"Article": 8, "title": "What can we do next to support our current ecosystem?"},
    {"Article": 9, "title": "Why you should care for your mental health"},
    {"Article": 10, "title": "The power of the african bull frog"}
]

# SEnds the article bank
socket.send_string(bank_name)
print(socket.recv_string())
# sends the article list
socket.send_string(json.dumps(article_bank))
print(socket.recv_string())
