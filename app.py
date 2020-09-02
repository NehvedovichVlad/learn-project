import socketserver
import settings
from xxx import MyHandler


def server_greet():
    print()
    print("*" * 40, "run", "*" * 40)
    print(f"PROJECT_DIR: \t{settings.PROJECT_DIR}")
    print(f"SERVER:      \thttp://localhost:{settings.PORT}")
    print("*" * 85)
    print()


if __name__ == "__main__":
    with socketserver.TCPServer(("", settings.PORT), MyHandler) as httpd:
        print("it works")
        httpd.serve_forever(poll_interval=1)
