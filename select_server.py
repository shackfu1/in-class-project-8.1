# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    s = socket.socket()
    connection = ('', port)
    s.bind(connection)
    s.listen()
    sock_set = {s}
    while True:
        ready_to_read, _, _ = select.select(sock_set, {}, {})
        for sock in ready_to_read:
            if sock == s:
                new_conn, addr = s.accept()
                addr, port = new_conn.getpeername()
                print("('" + str(addr) + "', " + str(port) + "): connected")
                sock_set.add(new_conn)
            else:
                data = sock.recv(40)
                addr, port = sock.getpeername()
                if data == b'':
                    sock_set.remove(sock)
                    sock.close()
                    print("('" + str(addr) + "', " + str(port) + "): disconnected")
                else:
                    print("('" + str(addr) + "', " + str(port) + ") " + str(len(data)) + " bytes: " + str(data))

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
