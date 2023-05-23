import socket
import threading

SOCKET_PORT = 8888


def waiting(sk, num):
    connected = False
    con = None

    while not connected:
        try:
            con, address = sk.accept()
        except BlockingIOError:
            pass
        if con:
            connected = True
            print(f'p{num}已连接')

    return con


def ready(con):
    start = False
    while not start:
        try:
            if con.recv(1024):
                start = True
        except Exception as e:
            pass


def transfer_piece_position(c1, c2):
    # 循环接收来自一个 socket 的消息，并转发给另一个 socket
    while True:
        try:
            msg = c1.recv(1024)
            if msg:
                c2.send(msg)
            if not msg:
                break
        except Exception as e:
            print(e)
            break


def main(con1, con2):
    con1.setblocking(True)
    con2.setblocking(True)
    t1 = threading.Thread(target=transfer_piece_position, args=(con1, con2))
    t2 = threading.Thread(target=transfer_piece_position, args=(con2, con1))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    hostname = socket.gethostname()
    localIp = socket.gethostbyname(hostname)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setblocking(False)

    socket.bind((f'{localIp}', SOCKET_PORT))
    socket.listen(2)

    print(f'{localIp}:{SOCKET_PORT}')

    connect1 = waiting(socket, 1)
    connect2 = waiting(socket, 2)
    ready(connect1)
    connect2.send('1'.encode('utf-8'))
    ready(connect2)
    connect1.send('1'.encode('utf-8'))

    main(connect1, connect2)
