# review_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class ReviewScreen(QWidget):
    def __init__(self, feedback_data, on_complete, scoring_manager):
        super().__init__()
        self.feedback_data = feedback_data
        self.on_complete = on_complete
        self.scoring_manager = scoring_manager

        layout = QVBoxLayout()

        title = QLabel("Review & Feedback")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        score = self.scoring_manager.get_score()
        total = self.scoring_manager.get_total_possible()

        score_label = QLabel(f"Your Score: {score}/{total}")
        layout.addWidget(score_label)

        # Give feedback based on score percentage
        if total > 0:
            percentage = (score / total) * 100
        else:
            percentage = 0

        if percentage > 80:
            msg = "Great job! You mastered most exercises."
        elif percentage > 50:
            msg = "Not bad, but you can improve. Check difficult exercises again."
        else:
            msg = "You struggled. Review the vocabulary and try again."

        feedback_label = QLabel(msg)
        layout.addWidget(feedback_label)

        layout.addWidget(QLabel("Recommendations:"))
        # If you have recommendations in feedback_data, show them:
        recs = ["- Review greetings daily", "- Practice pronouncing names", "- Repeat difficult exercises"]
        # You can replace with feedback_data from JSON if available
        for r in recs:
            layout.addWidget(QLabel(r))

        finish_btn = QPushButton("Finish Lesson")
        finish_btn.clicked.connect(self.on_complete)
        layout.addWidget(finish_btn)

        self.setLayout(layout)
