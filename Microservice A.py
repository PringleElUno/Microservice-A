import os
import json
from json import JSONDecodeError

import zmq

# Define the storage file, so that we can use the JSON
STORAGE_FILE = "article_storage.json"


# Loading or initialization of the storage for the articles
def load_storage():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as file:  # Read functions allow for the user to open the data/message
                return json.load(file)
        except json.JSONDecodeError:
            print("JSON file is corrupted, clearing storage file")
            return {}
    return {}


# A save storage function to call teh data
def save_storage(data):
    with open(STORAGE_FILE, 'w') as file:  # Allows for the user to write the saved storage data/message
        json.dump(data, file)

    # A set up to the ZEROMQ rep socket


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7979")  # Port of choosing is 7979
print(
    "Microservice is fully functional and live in the beautiful port of 7979...")  # Print statement for when the microservice is connected to the port

# define the storage so it can load a storage and call the whats inside the storage i.e the message
storage = load_storage()
current_key = None

while True:

        message = socket.recv_string()

        if message == "import":
            confirmation_message = "Ready to retrieve bank, send the name of the bank"
            socket.send_string(confirmation_message)
            message = socket.recv_string()
            # This will check for the key if it is stored and to retrieve it
            if message in storage:
                print(f"Retrieving articles for: {message}")
                print(f"Returned the articles: {json.dumps(storage[message])}")
                socket.send_string(json.dumps(storage[message]))  # ZeroMQ send string
                continue
            else:
                print("No bank corresponding to the name you sent.")
                confirmation_message = "None"
                socket.send_string(confirmation_message)
                continue
        if message == "export":
            confirmation_message = "Export request received, send the bank name"
            socket.send_string(confirmation_message)
            message = socket.recv_string()
            # if the key is not set correctly then we want to treat the message as the same
            if current_key is None:
                current_key = message
                socket.send_string("Got the Name!: Lets send that article list!")
            # The second message from the main program is the list of dictionaries (bank)
                message = socket.recv_string()
                article_list = json.loads(message)
                storage[current_key] = article_list
                try:
                    save_storage(storage)
                    print(f"Stored the articles for the key : {current_key}")
                    current_key = None
                    socket.send_string(f"The bank was stored!")
                except Exception as error:
                    print(f"Articles failed to save to storage for the key:  {current_key}")
                    current_key = None
                    socket.send_string(f"Articles failed to save to storage for the key:  {current_key}")
