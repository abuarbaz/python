import socket

host = socket.gethostname()

if host.startswith("EUP"):
    print(host)
elif host.startswith("Dev"):
    print(host)


