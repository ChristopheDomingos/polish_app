from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QButtonGroup
from PyQt6.QtCore import Qt

class QuizScreen(QWidget):
    def __init__(self, lesson_id, lesson_data, on_complete, progress_tracker, scoring_manager):
        super().__init__()
        self.lesson_id = lesson_id
        self.lesson_data = lesson_data
        self.on_complete = on_complete
        self.progress_tracker = progress_tracker
        self.scoring_manager = scoring_manager
        self.exercises = lesson_data.get_mini_quiz()
        self.current_index = 0
        self.attempts = 0

        self.layout = QVBoxLayout()

        title = QLabel("Mini-Quiz")
        title.setObjectName("titleLabel")
        self.layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.translation_label = QLabel()
        self.translation_label.setVisible(False)
        self.layout.addWidget(self.translation_label)
        self.show_translation_btn = QPushButton("Show Translation")
        self.show_translation_btn.clicked.connect(lambda: self.translation_label.setVisible(True))
        self.layout.addWidget(self.show_translation_btn)

        self.button_group = QButtonGroup(self)
        self.options_buttons = []
        for _ in range(4):
            rb = QRadioButton()
            self.button_group.addButton(rb)
            self.layout.addWidget(rb)
            self.options_buttons.append(rb)

        self.feedback = QLabel()
        self.layout.addWidget(self.feedback)

        self.hint_label = QLabel()
        self.hint_label.setVisible(False)
        self.layout.addWidget(self.hint_label)

        self.check_btn = QPushButton("Check")
        self.check_btn.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_btn)

        self.next_btn = QPushButton("Next")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_btn)

        self.setLayout(self.layout)
        self.display_question()

    def display_question(self):
        if self.current_index >= len(self.exercises):
            self.on_complete()
            return

        ex = self.exercises[self.current_index]
        self.attempts = 0
        self.feedback.setText("")
        self.hint_label.setVisible(False)
        self.next_btn.setEnabled(False)
        self.check_btn.setEnabled(True)

        self.question_label.setText(ex["question"])
        self.translation_label.setText(ex.get("translation", ""))
        self.translation_label.setVisible(False)

        for i, opt in enumerate(ex["options"]):
            self.options_buttons[i].setText(opt)
            self.options_buttons[i].setChecked(False)
            self.options_buttons[i].show()

        for i in range(len(ex["options"]), 4):
            self.options_buttons[i].hide()

        self.scoring_manager.add_exercise(points=10)

    def check_answer(self):
        ex = self.exercises[self.current_index]
        selected = None
        for rb in self.options_buttons:
            if rb.isChecked():
                selected = rb.text()
                break

        correct_answers = [ex["answer"]] if isinstance(ex["answer"], str) else ex["answer"]
        correct = self.lesson_data.check_answer(selected if selected else "", correct_answers)

        if correct:
            if self.attempts == 0:
                self.scoring_manager.correct_answer(first_try=True)
            else:
                self.scoring_manager.correct_answer(first_try=False)
            self.feedback.setText("Brawo! (Well done!)")
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            self.attempts += 1
            if self.attempts == 1:
                self.feedback.setText("Niepoprawne. Spróbuj jeszcze raz. (Incorrect. Try again.)")
                self.hint_label.setText("Hint: " + ex.get("hint", ""))
                self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
            else:
                self.feedback.setText(f"Poprawna odpowiedź: (The correct answer is:) {correct_answers[0]}")
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"quiz_{self.current_index}")

    def next_question(self):
        self.current_index += 1
        self.display_question()


