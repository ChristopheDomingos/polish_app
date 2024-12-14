# writing_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import unicodedata

class WritingPracticeScreen(QWidget):
    def __init__(self, lesson_id, lesson_data, on_complete, progress_tracker, scoring_manager):
        super().__init__()
        self.lesson_id = lesson_id
        self.lesson_data = lesson_data
        self.on_complete = on_complete
        self.progress_tracker = progress_tracker
        self.scoring_manager = scoring_manager
        
        # Load writing exercises
        self.exercises = self.lesson_data.get_writing_practice()
        self.current_index = 0
        self.attempts = 0  # Track attempts for the current exercise
        
        layout = QVBoxLayout()
        
        title = QLabel("Pisanie (Writing Practice)")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.prompt_label = QLabel()
        layout.addWidget(self.prompt_label)
        
        # Translation label if you have translations (optional)
        self.translation_label = QLabel()
        self.translation_label.setVisible(False)
        layout.addWidget(self.translation_label)
        
        self.show_translation_btn = QPushButton("Show Translation")
        self.show_translation_btn.clicked.connect(lambda: self.translation_label.setVisible(True))
        layout.addWidget(self.show_translation_btn)
        
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        
        self.feedback = QLabel()
        layout.addWidget(self.feedback)
        
        self.hint_label = QLabel()
        self.hint_label.setVisible(False)
        layout.addWidget(self.hint_label)
        
        self.check_btn = QPushButton("Check")
        self.check_btn.clicked.connect(self.check_answer)
        layout.addWidget(self.check_btn)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.next_exercise)
        layout.addWidget(self.next_btn)
        
        self.setLayout(layout)
        self.display_exercise()
    
    def display_exercise(self):
        if self.current_index >= len(self.exercises):
            # No more exercises
            self.on_complete()
            return
        
        self.attempts = 0
        self.feedback.setText("")
        self.hint_label.setVisible(False)
        self.next_btn.setEnabled(False)
        self.input_field.clear()
        self.check_btn.setEnabled(True)
        
        ex = self.exercises[self.current_index]
        self.prompt_label.setText(ex["prompt"])
        
        # If you have a translation field, set it here, else hide
        self.translation_label.setText(ex.get("translation", ""))
        self.translation_label.setVisible(False)
        
        self.expected_structure = ex["expected_structure"]  # array of strings
        self.exercise_hint = ex.get("hint", "")
        
        # Add this exercise for scoring
        self.scoring_manager.add_exercise(points=10)  # Adjust points as needed
    
    def normalize_text(self, text):
        # Remove diacritics and lower
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        text = ''.join(replacements.get(ch, ch) for ch in text)
        text = unicodedata.normalize('NFD', text)
        text = ''.join(ch for ch in text if not unicodedata.combining(ch))
        return ' '.join(text.lower().split())
    
    def check_answer(self):
        user_answer = self.input_field.text().strip()
        user_norm = self.normalize_text(user_answer)
        
        # Check if any of the expected phrases match (normalized)
        correct = False
        for exp in self.expected_structure:
            if self.normalize_text(exp) in user_norm:
                correct = True
                break
        
        if correct:
            # If correct on first or second try
            if self.attempts == 0:
                # full points
                self.scoring_manager.correct_answer(first_try=True)
            else:
                # fewer points if second try
                self.scoring_manager.correct_answer(first_try=False)
            self.feedback.setText("Dobrze! (Good!)")
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            # Incorrect attempt
            self.attempts += 1
            if self.attempts == 1:
                # First failure: show hint, allow second try
                self.feedback.setText("Niepoprawne. Spróbuj jeszcze raz.")
                if self.exercise_hint:
                    self.hint_label.setText("Hint: " + self.exercise_hint)
                    self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
                # Re-enable check to try again
                self.check_btn.setEnabled(True)
            else:
                # Second failure: reveal correct answer, allow to proceed
                correct_str = ", ".join(self.expected_structure)
                self.feedback.setText(f"Niestety, poprawna odpowiedź: {correct_str}")
                self.hint_label.setVisible(False)
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"writing_{self.current_index}")
    
    def next_exercise(self):
        self.current_index += 1
        self.display_exercise()
