import zmq

# Sets up our ZeroMQ 
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:7979") # remember we want to use the beautful 7979 port

# We send the bank name to retrieve it
bank_name = "SampleArticleBank"
socket.send_string(bank_name)

response = socket.recv_string()

print(f"Hey I got your data for the bank name! {bank_name}")

