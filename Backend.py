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
        print("WebSocket opened")
        clients.append(self)

    def on_message(self, message):
        for client in clients:
            client.write_message(message)

    def on_close(self):
        print("WebSocket closed")
        clients.remove(self)

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
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

