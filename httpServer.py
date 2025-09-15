import socket
import threading
import os
import datetime
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

HOST = '0.0.0.0'
PORT = 9090


def fetch_geo_info(ip_address):
    """접속 IP 기반 위치 정보를 조회한다. 실패 시 최소 정보만 반환."""
    # 무료 API: ip-api.com (비상업/제한적 용도)
    api_url = (
        f"http://ip-api.com/json/{ip_address}?lang=ko&fields="
        "status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
    )
    try:
        with urlopen(api_url, timeout=3) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            result = json.loads(data)
            if result.get("status") == "success":
                return {
                    "ip": result.get("query"),
                    "country": result.get("country"),
                    "region": result.get("regionName"),
                    "city": result.get("city"),
                    "zip": result.get("zip"),
                    "lat": result.get("lat"),
                    "lon": result.get("lon"),
                    "timezone": result.get("timezone"),
                    "isp": result.get("isp"),
                    "org": result.get("org"),
                    "as": result.get("as"),
                }
            else:
                return {"ip": ip_address, "error": result.get("message", "lookup_failed")}
    except (URLError, HTTPError, TimeoutError, ValueError):
        return {"ip": ip_address, "error": "lookup_error"}

def handle_client(conn, addr):
    try:
        request = conn.recv(1024).decode()
        print(request)
        
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

        client_ip = addr[0]

        # 위치 정보 제공 엔드포인트
        if path == "/location":
            geo = fetch_geo_info(client_ip)
            body = json.dumps(geo, ensure_ascii=False, indent=2).encode('utf-8')
            header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json; charset=utf-8\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            conn.sendall(header.encode('utf-8') + body)
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
            client_ip = addr[0]
            # 위치 요약 정보 조회 (로그용, 실패해도 서버 동작에는 영향 없음)
            geo = fetch_geo_info(client_ip)
            location_text = (
                f"{geo.get('country','?')} {geo.get('region','?')} {geo.get('city','?')}"
                if 'error' not in geo else "위치 조회 실패"
            )
            print(f"[접속] {client_ip}에서 {connect_time}에 접속함. 위치: {location_text}")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    main()
