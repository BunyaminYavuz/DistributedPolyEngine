import zmq

# Start the worker
context = zmq.Context()
worker_socket = context.socket(zmq.REP)
worker_socket.bind("tcp://*:5556")

while True:
    request = worker_socket.recv_json()
    coefficient = request["coefficient"]
    exponent = request["exponent"]
    x_value = request["x_value"]

    # Calculation
    result = coefficient * (x_value ** exponent)

    # Sending the result
    worker_socket.send_json({"result": result})
