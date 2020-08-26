import traceback
from http.server import SimpleHTTPRequestHandler

from mistakes import NotFound, MethodNotAllowed
from settings import CACHE_AGE
from utils import read_static, build_path
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
        path, file_path = get_path_with_file(self.path)
        content_type = get_content_type_from_file(file_path)

        handlers = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/style/": [self.handle_static, ["style.css", "text/css"]],
            "/image/": [self.handle_static, [f"img/{file_path}", content_type]],
            "/hello/": [self.handle_hello, []],
            "/0/": [self.handle_zde, []],
        }

        try:
            handler, args = handlers[path]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_hello(self):
        content = f"""
                <html>
                <head><title>XXX</title></head>
                <body>
                <h1>Hello World</h1>
                <p>PATH:{self.path}</p>
                </body>
                </html>
                """

        self.respond(content)

    def handle_zde(self):
        x = 1 / 0

    def handle_static(self, file_path, ct):
        content = read_static(file_path)
        self.respond(content, content_type=ct)

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
