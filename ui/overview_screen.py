from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class OverviewScreen(QWidget):
    def __init__(self, overview_data, on_complete):
        super().__init__()
        self.overview_data = overview_data
        self.on_complete = on_complete

        layout = QVBoxLayout()

        title = QLabel(self.overview_data.get("title", "Lesson Overview"))
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        duration = QLabel(f"Estimated Time: {self.overview_data.get('duration', 'N/A')}")
        layout.addWidget(duration)

        cultural_notes_label = QLabel("Cultural Notes:")
        cultural_notes_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(cultural_notes_label)
        c_notes = self.overview_data.get("cultural_notes", "")
        notes_label = QLabel(c_notes)
        layout.addWidget(notes_label)

        diff_label = QLabel(f"Difficulty: {self.overview_data.get('difficulty', 'N/A')}")
        layout.addWidget(diff_label)

        objectives_label = QLabel("Objectives:")
        objectives_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(objectives_label)
        for obj in self.overview_data.get("objectives", []):
            layout.addWidget(QLabel(f"• {obj}"))

        start_button = QPushButton("Start Lesson")
        start_button.clicked.connect(self.on_complete)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)