import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'  # 서버 IP (같은 PC면 127.0.0.1)
SERVER_PORT = 12345        # 서버 포트 (서버와 동일하게)

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                print("서버와의 연결이 종료되었습니다.")
                break
            decoded = message.decode()
            # 닉네임 입력 메시지일 때는 같은 줄에 입력할 수 있도록 처리
            if decoded.startswith("닉네임을 입력하세요"):
                sys.stdout.write(decoded)
                sys.stdout.flush()
            else:
                print(decoded)
        except:
            print("서버와의 연결이 끊어졌습니다.")
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(f"서버에 연결할 수 없습니다: {e}")
        sys.exit()

    # 메시지 수신 스레드 시작
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # 닉네임 입력 (닉네임 입력 메시지가 오면 바로 입력)
    nickname = input()
    sock.sendall(nickname.encode())

    while True:
        try:
            msg = input()
            if msg.lower() == 'quit':  # quit 입력 시 서버에 quit 전송 후 종료
                sock.sendall(msg.encode())
                print("채팅을 종료합니다.")
                break
            sock.sendall(msg.encode())
        except KeyboardInterrupt:
            print("\n채팅을 종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

    sock.close()

if __name__ == "__main__":
    main()