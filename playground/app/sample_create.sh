#!/bin/sh

curl -X POST http://127.0.0.1:8080/create \
     -H "Content-Type: application/json" \
     -d '{"queue_name": "sample_queue", "retention_time": 30}'

sleep 1

curl -X POST http://localhost:8080/send \
     -H "Content-Type: application/json" \
     -d '{"queue_name": "sample_queue", "message": "Hello, this is a test message! 1"}'

sleep 1

curl -X POST http://localhost:8080/send \
     -H "Content-Type: application/json" \
     -d '{"queue_name": "sample_queue", "message": "Hello, this is a test message! 2"}'

sleep 1
     
curl -X POST http://localhost:8080/send \
     -H "Content-Type: application/json" \
     -d '{"queue_name": "sample_queue", "message": "Hello, this is a test message! 3"}'

sleep 1

curl -X POST http://localhost:8080/send \
     -H "Content-Type: application/json" \
     -d '{"queue_name": "sample_queue", "message": "Hello, this is a test message! 4"}'

sleep 1

/usr/bin/python3 list_queues.py