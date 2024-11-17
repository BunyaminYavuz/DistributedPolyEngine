import zmq

# Start the server
context = zmq.Context()
request_socket = context.socket(zmq.REP)
request_socket.bind("tcp://*:5555")

# Start the workers
worker_sockets = []

def create_worker():
    worker_socket = context.socket(zmq.REQ)
    worker_socket.connect("tcp://localhost:5556")
    return worker_socket

# Receive requests from the user and dynamically adjust the number of workers
while True:
    request = request_socket.recv_json()
    terms = request["terms"]
    x_value = request["x_value"]
    num_terms = len(terms.split("+"))  # Number of polynomial terms

    # Dynamically adjust the number of workers
    while len(worker_sockets) < num_terms:
        worker_socket = create_worker()
        worker_sockets.append(worker_socket)

    # Send each term's coefficient and exponent to individual workers
    results = []
    for term in terms.split("+"):
        if "x" in term:
            coefficient, exponent = term.split("x")
            if "^" in exponent:
                exponent = int(exponent.split("^")[1])
            else:
                exponent = 1
            coefficient = int(coefficient)
            worker_socket = worker_sockets.pop(0)
            worker_socket.send_json({"coefficient": coefficient, "exponent": exponent, "x_value": x_value})
            result = worker_socket.recv_json()
            results.append(result)
            worker_sockets.append(worker_socket)
        else:
            # Constant term
            coefficient = int(term)
            worker_socket = worker_sockets.pop(0)
            worker_socket.send_json({"coefficient": coefficient, "exponent": 0, "x_value": x_value})
            result = worker_socket.recv_json()
            results.append(result)
            worker_sockets.append(worker_socket)

    # Calculate the total value of the polynomial by summing the results
    total_result = sum(result["result"] for result in results)
    request_socket.send_json({"result": total_result})
