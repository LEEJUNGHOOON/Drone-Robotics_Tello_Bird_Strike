```sequence
Title: Bird detection using drone

Drone -> Server: 1. Post image in png format
Server -> Drone: 2. Return which way to go

Note right of Server: 3. Bird detection using YOLO
Note left of Drone: 1. Convert video frames to images\n using ffmpeg
Note left of Drone: 2. Control Drone in response to the\n server message
Note over Drone, Server: Over network provided by Drone

```

