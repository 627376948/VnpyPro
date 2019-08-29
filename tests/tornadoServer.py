import json

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        d = {
            "ok": 100,
            "info": "我爱北京天安门",
            "status": True

        }
        json_str = json.dumps(d)
        print(type(json_str), json_str)
        print(self.settings)
        name = self.get_argument("name", "default_name")
        sex = self.get_argument("sex", "default_sex")

        print(f"{name}.{sex}")
        self.write(f"{name}:{sex}")

    def post(self):
        name = self.get_argument("name", "default_name")
        sex = self.get_argument("sex", "default_sex")

        print(f"{name}.{sex}")
        self.write(f"{name}:{sex}")


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)

    tornado.ioloop.IOLoop.instance().start()
