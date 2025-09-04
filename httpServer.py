import socket
import threading
import os
import datetime

HOST = '0.0.0.0'
PORT = 9090

def handle_client(conn, addr):
    try:
        request = conn.recv(1024).decode()
        if not request:
            conn.close()
            return
        # HTTP 요청의 첫 줄 파싱
        lines = request.splitlines()
        if len(lines) == 0:
            conn.close()
            return
        request_line = lines[0]
        method, path, _ = request_line.split()
        if method != 'GET':
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"
            conn.sendall(response.encode())
            conn.close()
            return

        # "/" 또는 "/index.html" 요청만 처리
        if path == "/" or path == "/index.html":
            # index.html 파일 경로를 현재 실행 폴더로 변경
            file_path = os.path.join(os.getcwd(), "index.html")
            try:
                with open(file_path, "rb") as f:
                    body = f.read()
                header = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                conn.sendall(header.encode('utf-8') + body)
            except FileNotFoundError:
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/plain; charset=utf-8\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "index.html 파일을 찾을 수 없습니다."
                )
                conn.sendall(response.encode('utf-8'))
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n"
                "Connection: close\r\n"
                "\r\n"
                "요청하신 페이지를 찾을 수 없습니다."
            )
            conn.sendall(response.encode('utf-8'))
    except Exception as e:
        error_msg = (
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"서버 오류: {e}"
        )
        conn.sendall(error_msg.encode('utf-8'))
    finally:
        conn.close()

def main():
    print(f"HTTP 서버가 {HOST}:{PORT}에서 시작되었습니다.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        while True:
            conn, addr = server_socket.accept()
            # 접속 시간과 IP 주소 출력
            connect_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[접속] {addr[0]}에서 {connect_time}에 접속함.")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    main()
