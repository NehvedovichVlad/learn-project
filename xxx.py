import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from utils import build_path
from chek import to_bytes

PORT = int(os.getenv("PORT", 8000))
print(PORT)

CACHE_AGE = 60 * 60 * 24

PROJECT_DIR = Path(__file__).parent.resolve()


class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self):
        return super().do_GET()


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

    def handle_style(self):
        css_file = PROJECT_DIR/"styles"/"style.css"
        if not css_file.exists():
            return self.handle_404()

        with css_file.open("r") as fp:
            css = fp.read()

        self.respond(css, content_type="text/css")

    def handle_image(self):
        img_file = PROJECT_DIR / "styles" / "img" / "logo.png"
        if not img_file.exists():
            return self.handle_404()

        with img_file.open("rb") as fp:
            img = fp.read()

        self.respond(img, content_type="image/png")

    def handle_404(self):
        msg = """NOT FOUND"""

        self.respond(msg, 404, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(message)))
        self.send_header("Cache-control", f"no-cache")
        self.end_headers()

        message = to_bytes(message)
        self.wfile.write(message)

    def do_GET(self):
        path = build_path(self.path)

        if path == "/":
            self.handle_root()
        elif path == "/style/":
            self.handle_style()
        elif path == "/hello/":
            self.handle_hello()
        elif path == "/image/":
            self.handle_image()
        else:
            self.handle_404()



if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it works")
        httpd.serve_forever(poll_interval=1)


























