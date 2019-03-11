#!/usr/bin/python


#Dependencies:
#python2.7
#pip install wheel
#pip install tornado


import tornado.websocket
import tornado.ioloop
import tornado.web


class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def broadcast(self, msg):
        messages.append(msg)
        for client in clients:
            client.write_message(msg)

    def open(self):
        clients.append(self)

    def on_message(self, message):
        
        
        if(message.startswith("name:")):
            print("Message recived: " + message)
            if(self in names):
                return
            names[self] = message[5:]
            for message in messages:
                self.write_message(message)
            self.broadcast('joined:' + message[5:])
        elif (message.startswith("knock")):
            print("Message recived: " + message)
            if(self in names):
                self.broadcast("knock:" + names[self])
        elif (message.startswith("reset")):
            print("Message recived: " + message)
            if(self in names):
                self.broadcast("reset:" + names[self])

    def on_close(self):
        clients.remove(self)
        if(self in names):
            self.broadcast('left:' + names[self])
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
    messages = []
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

