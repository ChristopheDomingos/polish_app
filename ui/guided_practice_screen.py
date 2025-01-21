from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QScrollArea, QHBoxLayout
)
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

        self.isPolishUI = True  # Initially Polish UI

        # Pre-define strings in both Polish and English
        self.polish_instruction = "Proszę, uzupełnić zdanie: (Please complete the sentence:)"
        self.english_instruction = "Please complete the sentence:"

        self.polish_try_again = "Nie całkiem. Spróbuj jeszcze raz. (Not quite. Try again.)"
        self.english_try_again = "Not quite. Try again."

        self.polish_correct = "Bardzo dobrze! (Very good!)"
        self.english_correct = "Very good!"

        self.polish_incorrect_prefix = "Niestety, poprawna odpowiedź: (Unfortunately, the correct answer is:)"
        self.english_incorrect_prefix = "Unfortunately, the correct answer is:"

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20,20,20,20)
        self.layout.setSpacing(20)

        self.title = QLabel("Ćwiczenia (Guided Practice)")
        self.title.setObjectName("titleLabel")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a button to toggle English/Polish UI
        self.toggle_lang_btn = QPushButton("Show English")
        self.toggle_lang_btn.clicked.connect(self.toggle_language)
        self.layout.addWidget(self.toggle_lang_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.instruction = QLabel(self.polish_instruction)
        self.layout.addWidget(self.instruction)

        self.sentence_label = QLabel()
        self.layout.addWidget(self.sentence_label)

        self.translation_label = QLabel()
        self.translation_label.setVisible(False)
        self.layout.addWidget(self.translation_label)

        self.show_translation_btn = QPushButton("Show Translation")
        self.show_translation_btn.clicked.connect(self.toggle_sentence_translation)
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

    def toggle_language(self):
        # Toggle the UI language
        self.isPolishUI = not self.isPolishUI
        self.update_ui_language()

    def update_ui_language(self):
        # Update instruction text
        if self.isPolishUI:
            self.instruction.setText(self.polish_instruction)
            self.toggle_lang_btn.setText("Show English")
            # Update any existing feedback or hint to Polish if they are visible
            self.update_feedback_language()
            self.update_hint_language()
        else:
            self.instruction.setText(self.english_instruction)
            self.toggle_lang_btn.setText("Show Polish")
            self.update_feedback_language()
            self.update_hint_language()

    def update_feedback_language(self):
        # Called after check_answer sets feedback in Polish, translate if needed
        current_text = self.feedback.text()
        if not current_text:
            return
        if self.isPolishUI:
            # If it's currently English, revert to Polish based on known phrases
            if "Not quite" in current_text:
                self.feedback.setText(self.polish_try_again)
            elif "Unfortunately" in current_text:
                # Extract correct answer from end of string if needed
                # The format: "Unfortunately, the correct answer is: X"
                # We can store last correct answer and re-set it
                # or re-check what we displayed last time.
                # We'll store last correct answer in self.last_correct_answer
                if hasattr(self, "last_correct_answer"):
                    self.feedback.setText(f"{self.polish_incorrect_prefix} {self.last_correct_answer}")
            elif "Very good!" in current_text and "Bardzo dobrze!" not in current_text:
                self.feedback.setText(self.polish_correct)
        else:
            # Convert Polish to English
            if self.polish_try_again in current_text:
                self.feedback.setText(self.english_try_again)
            elif self.polish_incorrect_prefix in current_text:
                # Extract answer from end
                prefix_len = len(self.polish_incorrect_prefix)
                answer = current_text[prefix_len:].strip()
                self.last_correct_answer = answer
                self.feedback.setText(f"{self.english_incorrect_prefix} {answer}")
            elif "Bardzo dobrze!" in current_text:
                self.feedback.setText(self.english_correct)

    def update_hint_language(self):
        # If hints are just shown once, and we know what the hint is.
        # The hint might be in Polish. If we want a hint translation, we must have a known translation.
        # The user didn't provide hint translations. We'll assume no hint translation available.
        # If you want to handle hints translation, add ex["hint_translation"] and handle similarly.
        # For now, leave hints as is. If user complains, we handle later.
        pass

    def toggle_sentence_translation(self):
        # Toggles the visibility of the sentence translation
        if self.translation_label.isVisible():
            self.translation_label.setVisible(False)
            self.show_translation_btn.setText("Show Translation")
        else:
            self.translation_label.setVisible(True)
            self.show_translation_btn.setText("Hide Translation")

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
        # Set translation if available
        ex_translation = ex.get("translation", "")
        self.translation_label.setText(ex_translation)
        if ex_translation:
            self.show_translation_btn.setVisible(True)
            self.translation_label.setVisible(False)
            self.show_translation_btn.setText("Show Translation")
        else:
            self.show_translation_btn.setVisible(False)

        self.check_btn.setEnabled(True)
        self.scoring_manager.add_exercise(points=10)

        if ex.get("audio"):
            self.audio_manager.play_audio(ex["audio"], url=ex.get("audio_url"))

        # Update UI language if toggled
        self.update_ui_language()

    def check_answer(self):
        ex = self.exercises[self.current_index]
        user_answer = self.input_field.text().strip()
        correct_answers = ex["answer"] if isinstance(ex["answer"], list) else [ex["answer"]]

        # Check correctness
        correct = self.lesson_data.check_answer(user_answer, correct_answers)

        if correct:
            if self.attempts == 0:
                self.scoring_manager.correct_answer(first_try=True)
            else:
                self.scoring_manager.correct_answer(first_try=False)
            # Polish feedback
            self.feedback.setText(self.polish_correct if self.isPolishUI else self.english_correct)
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            self.attempts += 1
            if self.attempts == 1:
                # first failure
                self.feedback.setText(self.polish_try_again if self.isPolishUI else self.english_try_again)
                self.hint_label.setText("Hint: " + ex.get("hint", ""))
                self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
            else:
                # second failure
                correct_answer_str = correct_answers[0]
                if self.isPolishUI:
                    self.feedback.setText(f"{self.polish_incorrect_prefix} {correct_answer_str}")
                else:
                    self.feedback.setText(f"{self.english_incorrect_prefix} {correct_answer_str}")
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"guided_{self.current_index}")

    def next_exercise(self):
        self.current_index += 1
        self.display_exercise()
