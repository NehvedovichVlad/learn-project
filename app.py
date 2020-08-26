import socketserver
import settings
from xxx import MyHandler

if __name__ == "__main__":
    with socketserver.TCPServer(("", settings.PORT), MyHandler) as httpd:
        print("it works")
        httpd.serve_forever(poll_interval=1)
