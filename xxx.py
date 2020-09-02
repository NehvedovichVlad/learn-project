import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler

from custom_types import Url
from mistakes import NotFound, MethodNotAllowed
from settings import CACHE_AGE
from utils import read_static, build_path, get_content_type, get_user_data
from chek import to_bytes


def get_path_with_file(url) -> tuple:
    path = build_path(url)
    parts = path.split("/")

    try:
        file_path = parts[2]
    except IndexError:
        file_path = None
    path = build_path(parts[1])
    path = f"/{path}" if path != "/" else path

    return path, file_path


def get_content_type_from_file(file_path: str) -> str:
    if not file_path:
        return "text/html"
    ext = file_path.split(".")[1].lower()
    content_type_by_extension = {
        "gif": "image/gif",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "png": "image/png",
        "svg": "image/svg+xml",
    }

    content_type = content_type_by_extension[ext]
    return content_type


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        url = Url.from_path(self.path)
        content_type = get_content_type(url.file_name)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/style/": [self.handle_static, ["style.css", "text/css"]],
            "/image/": [self.handle_static, [f"img/{url.file_name}", content_type]],
            "/hello/": [self.handle_hello, [url]],
            "/0/": [self.handle_zde, []],
        }

        try:
            handler, args = endpoints[url.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self, url):
        user = get_user_data(url.query_string)
        year = datetime.now().year - user.age

        content = f"""
           <html>
           <head><title>My Project :: Hello</title></head>
           <body>
           <h1 style="background-color:powderblue;">>Hello {user.name}!</h1>
           <h1 style="background-color:tomato;">>You was born at {year}!</h1>
           <p>path: {self.path}</p>
           <hr color="red" width="30000">

           <form>
               <label for="name-id">Your name:</label>
               <input type="text" name="name" id="name-id">
               <label for="age-id">Your age:</label>
               <input type="text" name="age" id="age-id">
               <button type="submit" id="greet-button-id">Greet</button>
           </form>
           <button onclick="document.location='default.asp'">Home Page</button>
           <a class="btn  btn--red" href="/">Home page</a>

           </body>
           </html>
           """

        self.respond(content)

    def handle_zde(self):
        x = 1 / 0
        print(x)

    def handle_static(self, file_path, content_type):
        content = read_static(file_path)
        self.respond(content, content_type=content_type)

    def handle_404(self):
        msg = """NOT FOUND"""
        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)
