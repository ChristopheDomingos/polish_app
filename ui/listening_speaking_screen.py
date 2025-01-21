# listening_speaking_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from utils.audio_manager import AudioManager
from lesson_loader import LessonLoader
import speech_recognition as sr

class ListeningSpeakingScreen(QWidget):
    def __init__(self, lesson_id, lesson_data, on_complete, progress_tracker, scoring_manager):
        super().__init__()
        self.lesson_id = lesson_id
        self.lesson_data = lesson_data
        self.on_complete = on_complete
        self.progress_tracker = progress_tracker
        self.scoring_manager = scoring_manager

        self.exercises = self.lesson_data.get_listening_and_speaking()
        self.current_index = 0
        self.attempts = 0
        self.audio_manager = AudioManager()

        layout = QVBoxLayout()

        title = QLabel("Słuchanie i Mówienie (Listening & Speaking)")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.instruction = QLabel()
        layout.addWidget(self.instruction)

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

        self.play_btn = QPushButton("Play Audio")
        self.play_btn.clicked.connect(self.play_audio)
        layout.addWidget(self.play_btn)

        self.speak_btn = QPushButton("Record Speech")
        self.speak_btn.clicked.connect(self.record_speech)
        layout.addWidget(self.speak_btn)

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
        self.current_ex = ex
        ex_type = ex["type"]

        # For dictation: show sentence and instructions
        # For speaking: also show the phrase user should say
        if ex_type == "dictation":
            # Display the sentence (instruction)
            self.instruction.setText(ex.get("sentence", "Listen and type what you hear."))
            self.reference_text = ex["answer"]  # correct answers
            self.translation_label.setText(ex.get("translation", ""))
            self.translation_label.setVisible(False)
        elif ex_type == "speaking":
            # Display the sentence (general instruction) and also the phrase (reference_text)
            base_instruction = ex.get("sentence", "Say the following phrase aloud:")
            phrase_to_speak = ex.get("reference_text", "")
            # Combine them so user sees what exactly to say
            self.instruction.setText(f"{base_instruction}\n{phrase_to_speak}")
            self.reference_text = [phrase_to_speak]  # Make it a list for consistency
            self.translation_label.setText(ex.get("translation", ""))
            self.translation_label.setVisible(False)

        self.scoring_manager.add_exercise(points=10)

    def play_audio(self):
        ex = self.current_ex
        if ex["type"] == "dictation":
            self.audio_manager.play_audio(ex.get("audio", ""), url=ex.get("audio_url"))
        elif ex["type"] == "speaking" and "audio" in ex:
            self.audio_manager.play_audio(ex["audio"], url=ex.get("audio_url"))

    def record_speech(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.feedback.setText("Speak now...")
                audio_data = r.listen(source, timeout=5)
                text = r.recognize_google(audio_data, language="pl-PL")
                self.input_field.setText(text)
                self.feedback.setText(f"You said: {text}")
        except sr.WaitTimeoutError:
            self.feedback.setText("No speech detected (timeout). Try again or press Check to attempt without speech.")
            self.check_btn.setEnabled(True)
        except sr.UnknownValueError:
            self.feedback.setText("Could not understand speech. Try again or press Check.")
            self.check_btn.setEnabled(True)
        except sr.RequestError:
            self.feedback.setText("Speech recognition service error. Try again or proceed.")
            self.check_btn.setEnabled(True)

    def check_answer(self):
        ex = self.current_ex
        ex_type = ex["type"]
        user_answer = self.input_field.text().strip()

        if ex_type == "dictation":
            correct_answers = ex["answer"]
        else:  # speaking
            correct_answers = self.reference_text

        is_correct = LessonLoader.check_answer(user_answer, correct_answers)

        if is_correct:
            if self.attempts == 0:
                self.scoring_manager.correct_answer(first_try=True)
            else:
                self.scoring_manager.correct_answer(first_try=False)
            self.feedback.setText("Świetnie! (Great!)")
            self.check_btn.setEnabled(False)
            self.next_btn.setEnabled(True)
        else:
            self.attempts += 1
            if self.attempts == 1:
                self.feedback.setText("Niepoprawne. Spróbuj jeszcze raz lub spróbuj nagrać ponownie. (Incorrect. Try again or record again.)")
                if "hint" in ex:
                    self.hint_label.setText("Hint: " + ex["hint"])
                    self.hint_label.setVisible(True)
                self.scoring_manager.wrong_answer(final_attempt=False)
                self.check_btn.setEnabled(True)
            else:
                # Second failure: reveal correct answer
                correct_str = ", ".join(correct_answers)
                self.feedback.setText(f"Niestety, poprawna odpowiedź: (Unfortunately, the correct answer is:) {correct_str}")
                self.hint_label.setVisible(False)
                self.check_btn.setEnabled(False)
                self.next_btn.setEnabled(True)
                self.scoring_manager.wrong_answer(final_attempt=True, exercise_id=f"listen_speak_{self.current_index}")

    def next_exercise(self):
        self.current_index += 1
        self.display_exercise()
