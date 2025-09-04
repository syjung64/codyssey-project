import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("채팅 클라이언트")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # GUI 구성
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="전송", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))

        self.nickname = simpledialog.askstring("닉네임", "닉네임을 입력하세요:", parent=master)
        if not self.nickname:
            master.destroy()
            return

        try:
            self.sock.connect((SERVER_HOST, SERVER_PORT))
        except Exception as e:
            messagebox.showerror("연결 오류", f"서버에 연결할 수 없습니다: {e}")
            master.destroy()
            return

        # 닉네임 전송
        self.sock.recv(1024)  # "닉네임을 입력하세요:" 메시지 수신 (버림)
        self.sock.sendall(self.nickname.encode())

        # 메시지 수신 스레드 시작
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024)
                if not message:
                    break
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, message.decode() + '\n')
                self.text_area.yview(tk.END)
                self.text_area.config(state='disabled')
            except:
                break
        self.sock.close()

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            try:
                self.sock.sendall(msg.encode())
                if msg.strip().lower() == 'quit':  # quit 입력 시 종료
                    self.master.destroy()
                    return
                self.entry.delete(0, tk.END)
            except:
                messagebox.showerror("오류", "서버와의 연결이 끊어졌습니다.")
                self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
