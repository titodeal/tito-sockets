from . import socket_server
import traceback


class ApplicationServer(socket_server.SocketServer):

    def handle_clients(self):
        connections = self.get_connections()
        if not connections:
            return

        print("=> Connections count process: ", len(connections))

        for idx, client in enumerate(connections):
            peername = client.getpeername()
            print(f"[{idx}] Start processing client:\n{peername}")

            msg = self.recv_messages(client, timeout=0)
            if not msg:
                continue

            print('=> recieved message: ', msg)
            if not (isinstance(msg, dict) and "method" in msg):
                response = f"!=>Recieved wrong format message\nMessage is: '{msg}'"
                print(response)
            else:
                try:
                    response = self.handle_massage(msg)
                except Exception as e:
                    traceback.print_exc()
                    response = str(e)
            self.send_data(client, response)
            print(f"=> End processing clinet: {peername}\n----------------")

    def handle_massage(self, msg):
        method = getattr(self, msg.get('method'))
        return method(*msg.get('args'))
