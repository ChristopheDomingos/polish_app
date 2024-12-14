from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from utils.audio_manager import AudioManager

class GuidedPracticeScreen(QWidget):
    def __init__(self, lesson_id, lesson_data, on_complete, progress_tracker, scoring_manager):
        super().__init__()
        self.lesson_id = lesson_id
        self.lesson_data = lesson_data
        self.on_complete = on_complete
        self.progress_tracker = progress_tracker
        self.scoring_manager = scoring_manager
        self.exercises = lesson_data.get_guided_practice()
        self.current_index = 0
        self.attempts = 0
        self.audio_manager = AudioManager()

        self.layout = QVBoxLayout()

        self.title = QLabel("Ćwiczenia (Guided Practice)")
        self.title.setObjectName("titleLabel")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.instruction = QLabel("Proszę, uzupełnić zdanie:")
        self.layout.addWidget(self.instruction)

        self.sentence_label = QLabel()
        self.layout.addWidget(self.sentence_label)

        # Translation on demand example
        self.translation_label = QLabel()
        self.translation_label.setVisible(False)
        self.layout.addWidget(self.translation_label)
        self.show_translation_btn = QPushButton("Show Translation")
        self.show_translation_btn.clicked.connect(lambda: self.translation_label.setVisible(True))
        self.layout.addWidget(self.show_translation_btn)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        self.feedback = QLabel()
        self.layout.addWidget(self.feedback)

        self.hint_label = QLabel()
        self.hint_label.setVisible(False)
        self.layout.addWidget(self.hint_label)

        self.check_btn = QPushButton("Check Answer")
        self.check_btn.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_btn)

        self.next_btn = QPushButton("Next")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.next_exercise)
        self.layout.addWidget(self.next_btn)

        self.setLayout(self.layout)
        self.display_exercise()

    def display_exercise(self):
        if self.current_index >= len(self.exercises):
            self.on_complete()
            return
        ex = self.exercises[self.current_index]
        self.attempts = 0
        self.feedback.setText("")
        self.hint_label.setVisible(False)
        self.next_btn.setEnabled(False)
        self.input_field.clear()

        sentence = ex["sentence"]
        self.sentence_label.setText(sentence)
        # If there's a translation field (not in json now), you could add one. For now:
        self.translation_label.setText(ex.get("translation", ""))
        self.translation_label.setVisible(False)

        self.check_btn.setEnabled(True)
        answers = ex["answer"]
        self.scoring_manager.add_exercise(points=10)

        if ex.get("audio"):
            self.audio_manager.play_audio(ex["audio"], url=ex.get("audio_url"))

    def check_answer(self):
        ex = self.exercises[self.current_index]
        user_answer = self.input_field.text().strip()
        correct_answers = ex["answer"] if isinstance(ex["answer"], list) else [ex["answer"]]
        
        # Check correctness
        correct = self.lesson_data.check_answer(user_answer, correct_answers)

        if correct:
            # correct
            if self.attempts == 0:
                # First try correct
                self.scoring_manager.correct_answer(first_try=True)
            else:
                # Second try correct
                self.scoring_manager.correct_answer(first_try=False)
            self.feedback.setText("Bardzo dobrze! (Very good!)")
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            # incorrect
            self.attempts += 1
            if self.attempts == 1:
                # first failure, show hint
                self.feedback.setText("Nie całkiem. Spróbuj jeszcze raz.")
                self.hint_label.setText("Hint: " + ex.get("hint", ""))
                self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
            else:
                # second failure
                self.feedback.setText(f"Niestety, poprawna odpowiedź: {ex['answer'][0]}")
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"guided_{self.current_index}")

    def next_exercise(self):
        self.current_index += 1
        self.display_exercise()
