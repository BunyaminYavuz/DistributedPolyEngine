from flask import Flask, render_template, request
import zmq
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get data from the user
    terms = request.form['terms']
    x_value = float(request.form['x_value'])

    # Establish connection
    context = zmq.Context()
    request_socket = context.socket(zmq.REQ)
    request_socket.connect("tcp://localhost:5555")

    # Start the timer
    start_time = time.time()

    # Send to the server
    request_socket.send_json({"terms": terms, "x_value": x_value})

    # Receive the results
    result = request_socket.recv_json()

    # Calculate the time
    end_time = time.time()
    computation_time = end_time - start_time

    # Send the result to the user
    return render_template('result.html', result=result, computation_time=computation_time)

if __name__ == '__main__':
    app.run(debug=True)
