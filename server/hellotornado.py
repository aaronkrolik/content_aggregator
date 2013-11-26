'''
annotated tutorial of tornado
'''
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    #what happens when we GET?
    def get(self):
        self.write("Hello, world; hello!")

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, test")

# instantiate a tornado web application with MainHandler mapped to /
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test", TestHandler)
])


if __name__ == "__main__":
    #listen on port 80
    application.listen(3813)
    #run the IOLoop
    tornado.ioloop.IOLoop.instance().start()

