# Client/Server script to check firewall ports
### Author: Ryan McGuire

## Config
In either server or client mode, a config file is specified containing 
server and client config entries. The yaml config can contain both, or only
one or the other.

A sample server definition looks like this (listening address is optional):
```
server:
  ports:
    - 0.0.0.0:22
    - 5432
    - 443
    - 8443
```

A sample client definition looks like this:
```
client:
  targets:
    127.0.0.1:
      ports:
        - 22
        - 5432
        - 443
        - 8443
    192.168.0.1:
      ports:
        - 22
        - 443
```

## Running
A python3 and python2 version are both provided.

To run in server mode:
```
check_fw.py -f <some_file.yaml> -v -s
```

To run in client mode:
```
check_fw.py -f <some_file.yaml> -v -c
```

## Output (Server)
![Server Output](/contrib/Screenshot_Server.png?raw=true "Server Output")
```
** Found server declaration, running ports...
        ** Port declarations found, ensuring listeners on ports:
                ** 192.168.0.181:22
                        ** Port ('192.168.0.181', 22) is listening
                ** 5432
                        ** Port ('0.0.0.0', 5432) not ready, starting...
                ** 9876
                        ** Port ('0.0.0.0', 9876) not ready, starting...
                ** 4526
                        ** Port ('0.0.0.0', 4526) not ready, starting...
** Ready to work, run the client...
** Received ping from ('192.168.0.181', 45980), sending pong...
** Received ping from ('192.168.0.181', 45546), sending pong...
** Received ping from ('192.168.0.181', 58778), sending pong...
** Received ping from ('192.168.0.181', 45996), sending pong...
** Received ping from ('192.168.0.181', 45562), sending pong...
** Received ping from ('192.168.0.181', 58794), sending pong...
```

## Output (Client)
![Server Output](/contrib/Screenshot_Client.png?raw=true "Client Output")
```
** Running port checks
        ** Scanning host 192.168.0.1
                ** Testing port 22      [OPENED]
                ** Testing port 443     [CLOSED]
        ** Scanning host 127.0.0.1
                ** Testing port 22      [OPENED]
                ** Testing port 5432    [CLOSED]
                ** Testing port 443     [CLOSED]
                ** Testing port 8443    [CLOSED]
```
