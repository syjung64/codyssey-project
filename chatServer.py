import socket
import threading

# 서버 정보 설정
HOST = '0.0.0.0'  # 모든 인터페이스에서 접속 허용
PORT = 12345      # 사용할 포트 번호

# 클라이언트 목록 저장
clients = []

def broadcast(message, sender_socket):
    """모든 클라이언트에게 메시지 전송 (보낸 사람 제외)"""
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    """클라이언트별 통신 처리"""
    try:
        # 1. 클라이언트로부터 닉네임을 먼저 받음
        client_socket.sendall("닉네임을 입력하세요: ".encode())
        nickname = client_socket.recv(1024).decode().strip()
        welcome_msg = f"{nickname}님이 입장하셨습니다.".encode()
        print(f"[접속] {addr} ({nickname}) 연결됨.")
        broadcast(welcome_msg, None)  # 모든 클라이언트에게 입장 알림
    except:
        clients.remove(client_socket)
        client_socket.close()
        return

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            decoded_msg = message.decode()
            if decoded_msg.strip().lower() == 'quit':  # quit 메시지 처리
                break
            print(f"[{nickname}] {decoded_msg}")
            broadcast(f"{nickname}: {decoded_msg}".encode(), client_socket)
        except:
            break
    print(f"[종료] {addr} ({nickname}) 연결 종료.")
    clients.remove(client_socket)
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[서버 시작] {HOST}:{PORT}에서 대기 중...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    main()
