#!/bin/bash

# refresh library
curl --data-binary '{ "jsonrpc": "2.0", "method": "VideoLibrary.Scan", "id": "mybash"}' -H 'content-type: application/json;' http://150.100.0.150:8080/jsonrpc
sleep 1
curl --data-binary '{ "jsonrpc": "2.0", "method": "AudioLibrary.Scan", "id": "mybash"}' -H 'content-type: application/json;' http://150.100.0.150:8080/jsonrpc
sleep 1

# clean non-existent content
curl --data-binary '{ "jsonrpc": "2.0", "method": "VideoLibrary.Clean", "id": "mybash"}' -H 'content-type: application/json;' http://150.100.0.150:8080/jsonrpc
sleep 1
curl --data-binary '{ "jsonrpc": "2.0", "method": "AudioLibrary.Clean", "id": "mybash"}' -H 'content-type: application/json;' http://150.100.0.150:8080/jsonrpc
sleep 1
