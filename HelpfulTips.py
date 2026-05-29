import json
import random
import zmq

PORT = 5555

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{PORT}")

print(f"Microservice started on port {PORT}...")
lastTip = ""
randomTip = ""

while True:
    rawBytes = socket.recv()

    print(f"Received raw bytes: {rawBytes}")

    try:
        # Parse the bytes to a string
        jsonData = json.loads(rawBytes.decode('utf-8'))

        # Extract the list from the wrapper
        tipsList = jsonData["tips"] # Note, tipsList must have a minimum of 2 unique tips!!!

        # Avoid picking the same tip back to back
        randomTip = lastTip
        while randomTip == lastTip:
            randomTip = random.choice(tipsList)
        lastTip = randomTip

    except Exception as err:
        print(f"Parsing error: {err}")
        randomTip = "Error processing tips list."

    # Pack the random tip into a key/value JSON structure matching your C# script
    response_dict = {"tip": randomTip}
    response_json_string = json.dumps(response_dict)

    socket.send(response_json_string.encode('utf-8'))