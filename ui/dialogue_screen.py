# dialogue_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup, QRadioButton
from PyQt6.QtCore import Qt
from lesson_loader import LessonLoader

class DialogueScreen(QWidget):
    def __init__(self, lesson_id, lesson_data, on_complete, progress_tracker, scoring_manager):
        super().__init__()
        self.lesson_id = lesson_id
        self.lesson_data = lesson_data
        self.on_complete = on_complete
        self.progress_tracker = progress_tracker
        self.scoring_manager = scoring_manager

        dialogue, self.interactive_choices = self.lesson_data.get_real_life_dialogue()
        self.dialogue_lines = dialogue
        self.current_index = 0
        self.attempts = 0

        self.layout = QVBoxLayout()

        title = QLabel("Real-Life Dialogue")
        title.setObjectName("titleLabel")
        self.layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Show the dialogue scenario
        self.dialogue_label = QLabel()
        self.layout.addWidget(self.dialogue_label)

        self.choice_prompt = QLabel()
        self.layout.addWidget(self.choice_prompt)

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
        self.next_btn.clicked.connect(self.next_dialogue)
        self.layout.addWidget(self.next_btn)

        self.setLayout(self.layout)
        self.display_dialogue()

    def display_dialogue(self):
        if self.current_index >= len(self.interactive_choices):
            # Finished all choices
            self.on_complete()
            return
        self.attempts = 0
        self.feedback.setText("")
        self.hint_label.setVisible(False)
        self.next_btn.setEnabled(False)
        self.check_btn.setEnabled(True)

        # Show the main dialogue scenario above (if you want)
        scenario_text = ""
        for line in self.dialogue_lines:
            scenario_text += f"{line['speaker']}: {line['text']}\n"
        self.dialogue_label.setText(scenario_text.strip())

        ex = self.interactive_choices[self.current_index]
        # ex has "prompt", "options", and "answer" now, no "correct_option"
        self.choice_prompt.setText(ex["prompt"])

        # Clear old options
        for rb in self.options_buttons:
            rb.hide()

        # Set new options
        for i, opt in enumerate(ex["options"]):
            self.options_buttons[i].setText(opt)
            self.options_buttons[i].show()
            self.options_buttons[i].setChecked(False)

        # Add to scoring
        self.scoring_manager.add_exercise(points=10)

        self.exercise = ex

    def check_answer(self):
        ex = self.exercise
        selected = None
        for rb in self.options_buttons:
            if rb.isChecked():
                selected = rb.text().strip()
                break

        correct_answers = ex["answer"]  # This is now an array of correct answers
        is_correct = LessonLoader.check_answer(selected if selected else "", correct_answers)

        if is_correct:
            if self.attempts == 0:
                self.scoring_manager.correct_answer(first_try=True)
            else:
                self.scoring_manager.correct_answer(first_try=False)
            self.feedback.setText("Dobrze! (Good!)")
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            # Incorrect
            self.attempts += 1
            if self.attempts == 1:
                self.feedback.setText("Niepoprawne. Spróbuj jeszcze raz. (Incorrect. Try again.)")
                if "hint" in ex:
                    self.hint_label.setText("Hint: " + ex["hint"])
                    self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
                self.check_btn.setEnabled(True)
            else:
                # Second attempt, reveal correct answer
                correct_str = ", ".join(correct_answers)
                self.feedback.setText(f"Niestety, poprawna odpowiedź: (Unfortunately, the correct answer is:) {correct_str}")
                self.hint_label.setVisible(False)
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"dialogue_{self.current_index}")

    def next_dialogue(self):
        self.current_index += 1
        self.display_dialogue()

