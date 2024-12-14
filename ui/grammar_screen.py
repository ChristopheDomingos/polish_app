from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from utils.audio_manager import AudioManager

class GrammarScreen(QWidget):
    def __init__(self, grammar_data, on_complete):
        super().__init__()
        self.grammar_data = grammar_data
        self.on_complete = on_complete
        self.audio_manager = AudioManager()

        layout = QVBoxLayout()

        title = QLabel("Grammar Insight")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        explanation = self.grammar_data.get("explanation", "")
        explanation_label = QLabel(explanation)
        layout.addWidget(explanation_label)

        # If we had a translation for explanation:
        # If grammar_data.get("translation"):
        #     self.translation_label = QLabel(grammar_data["translation"])
        #     self.translation_label.setVisible(False)
        #     layout.addWidget(self.translation_label)
        #     trans_btn = QPushButton("Show Translation")
        #     trans_btn.clicked.connect(lambda: self.translation_label.setVisible(True))
        #     layout.addWidget(trans_btn)

        for table_data in self.grammar_data.get("tables", []):
            table_title = QLabel(table_data["title"])
            layout.addWidget(table_title)

            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])

            table_widget = QTableWidget(len(rows), len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            for r_idx, row_data in enumerate(rows):
                for c_idx, cell_data in enumerate(row_data):
                    table_widget.setItem(r_idx, c_idx, QTableWidgetItem(cell_data))
            layout.addWidget(table_widget)

        if self.grammar_data.get("audio_explanation"):
            audio_btn = QPushButton("Play Grammar Explanation")
            audio_btn.clicked.connect(lambda: self.audio_manager.play_audio(self.grammar_data["audio_explanation"], url=self.grammar_data.get("audio_explanation_url")))
            layout.addWidget(audio_btn)

        continue_btn = QPushButton("Continue")
        continue_btn.clicked.connect(self.on_complete)
        layout.addWidget(continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)