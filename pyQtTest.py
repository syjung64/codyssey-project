from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QCheckBox, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QProgressBar, QGroupBox, QHBoxLayout, QGridLayout, QMainWindow
)

# 1. App 객체 생성
app = QApplication([])

# 2. 창 생성
window = QWidget()
#window = QMainWindow()

window.setWindowTitle("QVBoxLayout + QGridLayout 위젯 예시")

# 3. 레이아웃 생성
layout = QVBoxLayout()

# 4-1. 버튼, 레이블, 라인에디터, 텍스트에디터터 위젯 추가
btn = QPushButton('test')
layout.addWidget(btn)

layout.addWidget(QLabel("1. QLabel (텍스트 출력)"))
text = QLineEdit("2. QLineEdit (한 줄 입력)")
layout.addWidget(text)
layout.addWidget(QTextEdit("3. QTextEdit (여러 줄 입력)"))

# 4-2. 체크박스 위젯 추가
checkbox = QCheckBox("4. QCheckBox 선택")
layout.addWidget(checkbox)

# 4-3. 콤보 박스 위젯 추가
combo = QComboBox()
combo.addItems(["A", "B", "C"])
layout.addWidget(QLabel("5. QComboBox (드롭다운 선택)"))
layout.addWidget(combo)

# 4-4. 테이블 위젯 추가
table = QTableWidget(2, 2)
table.setItem(0, 0, QTableWidgetItem("6.1"))
table.setItem(0, 1, QTableWidgetItem("6.2"))
table.setItem(1, 0, QTableWidgetItem("6.3"))
table.setItem(1, 1, QTableWidgetItem("6.4"))
layout.addWidget(QLabel("6. QTableWidget (테이블)"))
layout.addWidget(table)

# 4-5. 프로그레스 바 웨젯 추가
progress = QProgressBar()
progress.setValue(70)
layout.addWidget(QLabel("7. QProgressBar (진행률)"))
layout.addWidget(progress)

layout.addWidget(QPushButton("8. QPushButton (버튼)"))

# 4-6. QGroupBox 안에 QGridLayout 삽입
group_box = QGroupBox("9. QGridLayout 예시 (입력 양식 폼)")
grid_layout = QGridLayout()
grid_layout.addWidget(QLabel("이름:"), 0, 0)
grid_layout.addWidget(QLineEdit(), 0, 1)

grid_layout.addWidget(QLabel("이메일:"), 1, 0)
grid_layout.addWidget(QLineEdit(), 1, 1)

grid_layout.addWidget(QLabel("생년월일:"), 2, 0)
grid_layout.addWidget(QLineEdit(), 2, 1)

grid_layout.addWidget(QPushButton("제출"), 3, 0, 1, 2)  # 병합

group_box.setLayout(grid_layout)
layout.addWidget(group_box)

# 5. 최종 레이아웃 적용
window.setLayout(layout)

# 6. 시스턴-슬롯 연결
btn.clicked.connect(lambda: text.setText('눌렸음'))

#7. 창 띄우기
window.show()

# 8. 이벤트 루프 실행
app.exec_()
