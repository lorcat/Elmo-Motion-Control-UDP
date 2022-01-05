# remote controller parameters - IP & PORT, defaul.t port is 5001
# please adjust the hostname for your configuration
CONTROLLER_HOST, CONTROLLER_PORT = "192.168.58.232", 5001

import socket
import queue
import time

def profile(func):
    def wrap(*args, **kwargs):
        ts = time.time()
        res = func(*args, **kwargs)
        print("\nFunction ({}) took ({:6.3f}s)".format(func.__name__, time.time() - ts))
        return res
    return wrap

def communicate_with_lm():
    """
    Proof of principle function in order to control Gold Drive in Elmo description
    Start up a UDP server and communicate with a LabMotion DB3.6 controller
    Pity - no TCP/IP here..
    """

     # Tango server params - host
    SERVER_HOST = ""                        # Tango Server as UDP server
    SERVER_PORT = 20000                     # port can be any, if 20000 is bound, can use other
                                            # Elmo Application Studio II typically starts with port number 20000
                                            # controller supports multiple non blocking connections, as long as they
                                            # orifinate from a different port

    # Server is UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind a port, if port is bound, use another one
    bportsearch = True
    while bportsearch:
        try:
            sock.bind((SERVER_HOST, SERVER_PORT))
            bportsearch = False
        except OSError:
            SERVER_PORT += 1

    print("Server started with parameters ({}:{})".format(SERVER_HOST, SERVER_PORT))

    q = queue.Queue()
    q.put(b"VR\r")      # Retrieves Controller info
    q.put(b"AA[20]\r")  # Retrieves IP of the controller
    q.put(b"AA[21]\r")  # Retrieves Network of the controller
    q.put(b"AA[22]\r")  # Retrieves Gateway of the controller

    cnt = 0

    # Sending the messages to the controller and receive the feedback
    try:
        while True:
            # message to a controller
            msg = q.get(block=False)

            data = send(sock, msg)

            print("-> Sent {}".format(msg))
            print("<- Received: {}".format(data))

            cnt = cnt + 1
    except queue.Empty:
        print("\nAll messages sent ({}).".format(cnt))

    sock.close()

@profile
def send(sock, msg):
    """
    Function performing communication - sending a command and receiving a response
    :param sock: socket.socket()
    :param msg: bytearray()
    :return:
    """
    global CONTROLLER_HOST, CONTROLLER_PORT
    sock.sendto(msg, (CONTROLLER_HOST, CONTROLLER_PORT))

    # need to recover only read data, not data setting the values
    data, addr = sock.recvfrom(1024)
    return data

if __name__ == "__main__":
    communicate_with_lm()
