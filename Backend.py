#!/usr/bin/python


#Dependencies:
#python2.7
#pip install wheel
#pip install tornado


import tornado.websocket
import tornado.ioloop
import tornado.web


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)

    def on_message(self, message):
        print("Message recived: " + message)
        if(message.startswith("name:")):
            if(self in names):
                return
            names[self] = message[5:]
            for client in clients:
                client.write_message('joined:' + message[5:])
        elif (message.startswith("knock:")):
            for client in clients:
                client.write_message(message)

    def on_close(self):
        clients.remove(self)

        for client in clients:
            client.write_message('left:' + names[self])
        del names[self]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class GameHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("game.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/game", GameHandler),
        (r"/ws", EchoWebSocket),
    ])

if __name__ == "__main__":
    clients = []
    names = {}
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

