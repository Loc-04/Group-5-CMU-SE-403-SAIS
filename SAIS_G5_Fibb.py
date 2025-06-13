# http://127.0.0.1:5000/api/fibonacci?n=10 chọn số lượng số Fibonacci muốn tính qua n = 
#queue.PriorityQueue dùng để quản lý sự kiện với độ ưu tiên
#threading.Thread dùng để xử lý sự kiện trong các luồng riêng biệt
#time.sleep(0.1) dùng để tối ưu tài nguyên CPU 
import threading
import time
import queue
from flask import Flask, jsonify, request

app = Flask(__name__)

# Class to represent an event with priority
class Event:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
    
    def __lt__(self, other):
        return self.priority > other.priority  # Higher priority should come first

# Function to simulate processing an event
def process_event(event):
    time.sleep(0.1)  # Simulate work
    print(f"Processing Event: {event.description} with Priority: {event.priority}")

# Function to handle event prioritization and concurrency
def event_processing():
    # Create a priority queue to prioritize events
    event_queue = queue.PriorityQueue()
    
    # Add events with different priorities
    event_queue.put(Event(5, "Low Priority Event"))
    event_queue.put(Event(1, "High Priority Event"))
    event_queue.put(Event(3, "Medium Priority Event"))

    # Process events in order of priority (highest first)
    threads = []
    while not event_queue.empty():
        event = event_queue.get()
        # Introduce concurrency by processing events in separate threads
        t = threading.Thread(target=process_event, args=(event,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

# Fibonacci function to return sequence up to nth number
def fibonacci(n):
    a, b = 0, 1
    sequence = []
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# API route to test Fibonacci calculation
@app.route('/api/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        n = int(request.args.get('n', 10))  # Default to 10 if no input provided
        result = fibonacci(n)
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "Invalid input. Please provide a valid integer."}), 400

if __name__ == '__main__':
    print("Starting event processing with priority and concurrency optimization...\n")
    event_processing()  # Run event processing
    
    # Start the Flask API
    app.run(debug=True, host='0.0.0.0', port=5000)
