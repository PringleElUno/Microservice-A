import os
import json
import zmq

# Define the storage file, so that we can use the JSON 
STORAGE_FILE = "article_storage.json"

# Loading or intilization of the storage for the articles
def load_storage():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as file: # Read functions allow for the user to open the data/message
            return json.load(file)
    return {}
    
# A save storage function to call teh data
def save_storage(data):
    with open(STORAGE_FILE, 'w') as file: # Allows for the user to write the saved storage data/message
        json.dump(data, file) 

# A set up to the ZEROMQ rep socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7979") #Port of choosing is 7979
print("Microservice is fully functional and live in the beautiful port of 7979...") # Print statement for when the microservice is connected to the port

# define the storage so it cna load a storage and call the whats inside the storage i.e the message
storage = load_storage()
current_key = None


while True:
    try: # allows for crashs to be handled without crashing complete server and constant looping incase of incorrect json files
        message = socket.recv_string()

        # This will check for the key if it is stored and to retrieve it
        if message in storage:
            print(f"Retrieving articles for: {message}")
            print(f"Returned the articles: {json.dumps(storage[message])}")
            socket.send_string(json.dumps(storage[message])) # ZeroMQ send string
            continue
        
        # if the key is not set correctly then we want to treat the message as the same
        if current_key is None:
            current_key = message
            socket.send_string("Got the Name!: Lets send that article list!")
        # The second message with regards to the list of dictionaries
        else:
            article_list = json.loads(message)
            storage[current_key] = article_list
            save_storage(storage)
            print(f"Stored the articles in the: {current_key}")
            current_key = None
            socket.send_string("The articles was stored!")
    # Our exception error whenever the server reaches a error, the try statement embedded will aid the server to not crash completely!
    except Exception as error:
        socket.send_string(f"Error! {str(error)}")
        current_key = None