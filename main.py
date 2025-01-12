import sys
import random
from PyQt6.QtWidgets import QApplication, QStackedWidget
from lesson_loader import LessonLoader
from utils.resource_manager import ResourceManager
from utils.progress_tracker import ProgressTracker
from utils.scoring_manager import ScoringManager
from ui.welcome_screen import WelcomeScreen
from ui.grammar_screen import GrammarScreen
from ui.vocabulary_screen import VocabularyScreen
from ui.guided_practice_screen import GuidedPracticeScreen
from ui.writing_screen import WritingPracticeScreen
from ui.listening_speaking_screen import ListeningSpeakingScreen
from ui.dialogue_screen import DialogueScreen
from ui.quiz_screen import QuizScreen
from ui.review_screen import ReviewScreen

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polish Lessons App")
        self.setGeometry(100, 100, 900, 600)

        # For now only two lesson
        self.lessons = {
            "lesson 0": "lessons/lesson_0.json",
            "Lesson 1": "lessons/lesson_1.json",
            "Lesson 2": "lessons/lesson_2.json",
            "Lesson 3": "lessons/lesson_3.json",
            "Lesson 4": "lessons/lesson_4.json",
            "Lesson 5": "lessons/lesson_5.json",
            "Lesson 6": "lessons/lesson_6.json"
        }

        self.progress_tracker = ProgressTracker()
        self.res_manager = ResourceManager()
        self.scoring_manager = ScoringManager()

        # Welcome Screen
        self.welcome_screen = WelcomeScreen(self.lessons.keys(), self.load_lesson)
        self.addWidget(self.welcome_screen)
        self.setCurrentWidget(self.welcome_screen)

    def load_lesson(self, lesson_name):
        lesson_file = self.lessons[lesson_name]
        self.lesson_data = LessonLoader(lesson_file)
        
        # Prepare resources (like vocab images)
        self.prepare_resources()

        # Load screens in order:
        # Grammar -> Vocab -> Guided -> Writing -> Listening -> Dialogue -> Quiz -> Review
        self.grammar = GrammarScreen(self.lesson_data.get_grammar_insight(), self.next_screen)
        self.addWidget(self.grammar)

        self.vocab = VocabularyScreen("lesson_1", self.lesson_data.get_vocabulary(), self.next_screen, self.progress_tracker, self.scoring_manager, self.lesson_data)
        self.addWidget(self.vocab)

        self.guided = GuidedPracticeScreen("lesson_1", self.lesson_data, self.next_screen, self.progress_tracker, self.scoring_manager)
        self.addWidget(self.guided)

        self.writing = WritingPracticeScreen("lesson_1", self.lesson_data, self.next_screen, self.progress_tracker, self.scoring_manager)
        self.addWidget(self.writing)

        self.listen_speak = ListeningSpeakingScreen("lesson_1", self.lesson_data, self.next_screen, self.progress_tracker, self.scoring_manager)
        self.addWidget(self.listen_speak)

        self.dialogue = DialogueScreen("lesson_1", self.lesson_data, self.next_screen, self.progress_tracker, self.scoring_manager)
        self.addWidget(self.dialogue)

        self.quiz = QuizScreen("lesson_1", self.lesson_data, self.next_screen, self.progress_tracker, self.scoring_manager)
        self.addWidget(self.quiz)

        self.review = ReviewScreen(self.lesson_data.get_review_feedback(), self.return_to_start, self.scoring_manager)
        self.addWidget(self.review)

        # Move to grammar first after welcome
        self.setCurrentWidget(self.grammar)

    def prepare_resources(self):
        # Download/generate images for vocabulary if needed
        vocab = self.lesson_data.get_vocabulary()
        for v in vocab:
            if "image" in v and v["image"]:
                self.res_manager.ensure_resource(
                    v["image"],
                    url=v.get("image_url"),
                    text_for_audio=v["word"],
                    is_image=True
                )

    def next_screen(self):
        current = self.currentIndex()
        if current < self.count() - 1:
            self.setCurrentIndex(current + 1)
        else:
            self.return_to_start()

    def return_to_start(self):
        # Go back to welcome screen
        self.setCurrentWidget(self.welcome_screen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("style.qss", "r", encoding="utf-8") as f:
        qss = f.read()
    app.setStyleSheet(qss)

    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())