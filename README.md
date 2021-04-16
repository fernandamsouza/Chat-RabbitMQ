# Chat-RabbitMQ
Chat Rabbit with file transfer. The Chat Client reads (allocates in memory) a file from the local disk and sends it to the server. The server, in turn, receives the file, and writes it to the local disk. To receive messages, clients must consult the server from time to time (polling).
