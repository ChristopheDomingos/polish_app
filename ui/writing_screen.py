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
        
        self.exercises = self.lesson_data.get_writing_practice()
        self.current_index = 0
        self.attempts = 0

        self.isPolishPrompt = True
        self.original_prompt = ""
        self.prompt_translation = ""

        # A simple dictionary of common Polish phrases we might expect.
        # Add as many as needed.
        self.translations_dict = {
            "Jak masz na imię?": "What is your name? (informal)",
            "Proszę, uzupełnić zdanie:": "Please complete the sentence:",
            "Niepoprawne. Spróbuj jeszcze raz.": "Incorrect. Try again.",
            "Niestety, poprawna odpowiedź:": "Unfortunately, the correct answer is:",
            # Add any commonly used instructions or hints here...
        }

        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)

        title = QLabel("Pisanie (Writing Practice)")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.prompt_label = QLabel()
        layout.addWidget(self.prompt_label)
        
        self.show_prompt_translation_btn = QPushButton("Show Prompt Translation")
        self.show_prompt_translation_btn.clicked.connect(self.toggle_prompt_translation)
        layout.addWidget(self.show_prompt_translation_btn)

        # We remove self.translation_label since now we rely on toggling prompt directly from dictionary
        # If you want an exercise-specific translation (like from ex["translation"]), handle similarly.
        
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
            self.on_complete()
            return
        
        self.attempts = 0
        self.feedback.setText("")
        self.hint_label.setVisible(False)
        self.next_btn.setEnabled(False)
        self.input_field.clear()
        self.check_btn.setEnabled(True)
        
        ex = self.exercises[self.current_index]
        self.original_prompt = ex["prompt"]
        self.isPolishPrompt = True
        self.update_prompt_label(self.original_prompt)

        self.expected_structure = ex["expected_structure"]
        self.exercise_hint = ex.get("hint", "")
        
        self.scoring_manager.add_exercise(points=10)

        # If you have a separate translation for the prompt from ex["translation"],
        # you could integrate it similarly by toggling between original_prompt and ex["translation"].

    def update_prompt_label(self, text):
        self.prompt_label.setText(text)

    def toggle_prompt_translation(self):
        if self.isPolishPrompt:
            # Attempt to translate prompt from dictionary
            translation = self.translations_dict.get(self.original_prompt, "")
            if not translation:
                translation = "No translation available."
            self.update_prompt_label(translation)
            self.show_prompt_translation_btn.setText("Show Polish")
            self.isPolishPrompt = False
        else:
            # Show original Polish again
            self.update_prompt_label(self.original_prompt)
            self.show_prompt_translation_btn.setText("Show Prompt Translation")
            self.isPolishPrompt = True

    def normalize_text(self, text):
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
        
        correct = False
        for exp in self.expected_structure:
            if self.normalize_text(exp) in user_norm:
                correct = True
                break
        
        if correct:
            if self.attempts == 0:
                self.scoring_manager.correct_answer(first_try=True)
            else:
                self.scoring_manager.correct_answer(first_try=False)
            self.feedback.setText("Dobrze! (Good!)")
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            self.attempts += 1
            if self.attempts == 1:
                self.feedback.setText("Niepoprawne. Spróbuj jeszcze raz.")
                if self.exercise_hint:
                    self.hint_label.setText("Hint: " + self.exercise_hint)
                    self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
                self.check_btn.setEnabled(True)
            else:
                correct_str = ", ".join(self.expected_structure)
                self.feedback.setText(f"Niestety, poprawna odpowiedź: {correct_str}")
                self.hint_label.setVisible(False)
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"writing_{self.current_index}")
    
    def next_exercise(self):
        self.current_index += 1
        self.display_exercise()


