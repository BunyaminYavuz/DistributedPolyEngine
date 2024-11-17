import zmq
import time

# Taking the polynomial coefficients, exponents, and the value of x from the user
terms = input("Enter the polynomial terms (e.g. 3x^2+2x+4): ")
x_value = int(input("Enter the value of x: "))

# Sending to the server
context = zmq.Context()
request_socket = context.socket(zmq.REQ)
request_socket.connect("tcp://localhost:5555")
start_time = time.time()
request_socket.send_json({"terms": terms, "x_value": x_value})
end_time = time.time()

# Receiving the results
result = request_socket.recv_json()
print(f"Final result: {result} computation time: {end_time - start_time}")
