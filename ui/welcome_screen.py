from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
from PyQt6.QtCore import Qt

class WelcomeScreen(QWidget):
    def __init__(self, lessons, on_lesson_selected):
        super().__init__()
        self.lessons = lessons
        self.on_lesson_selected = on_lesson_selected

        layout = QVBoxLayout()

        title = QLabel("Welcome to Polish Lessons!")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        intro = QLabel("This application helps you learn Polish through grammar insights, vocabulary, exercises, listening, speaking, dialogues, and quizzes. Select a lesson below to begin:")
        layout.addWidget(intro)

        self.lesson_list = QListWidget()
        for lesson_name in self.lessons:
            self.lesson_list.addItem(lesson_name)
        layout.addWidget(self.lesson_list)

        start_btn = QPushButton("Start Selected Lesson")
        start_btn.clicked.connect(self.start_lesson)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def start_lesson(self):
        selected_item = self.lesson_list.currentItem()
        if selected_item:
            self.on_lesson_selected(selected_item.text())
        else:
            QMessageBox.warning(self, "No Lesson Selected", "Please select a lesson to start.")