# vocabulary_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QWidget as QW, QAbstractItemView
)
from PyQt6.QtCore import Qt
from utils.audio_manager import AudioManager

class VocabularyScreen(QWidget):
    def __init__(self, lesson_id, vocab_data, on_complete, progress_tracker, scoring_manager, lesson_data):
        super().__init__()
        self.lesson_id = lesson_id
        self.vocab_data = vocab_data
        self.on_complete = on_complete
        self.progress_tracker = progress_tracker
        self.scoring_manager = scoring_manager
        self.lesson_data = lesson_data
        self.audio_manager = AudioManager()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("Słownictwo (Vocabulary Introduction)")
        title.setObjectName("titleLabel")
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QW()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(20)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Word", "Show Translation", "Play"])
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # Show vertical header (row numbers)
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setMinimumWidth(50)  # Enough width for two-digit row numbers

        table.setRowCount(len(self.vocab_data))
        for r_idx, item in enumerate(self.vocab_data):
            word_item = QTableWidgetItem(item["word"])
            # Store data for toggling translation
            word_item.setData(Qt.ItemDataRole.UserRole, {
                "polish": item["word"],
                "english": item["translation"],
                "isPolish": True
            })
            table.setItem(r_idx, 0, word_item)

            show_btn = QPushButton("Show Translation")
            show_btn.clicked.connect(lambda ch, row=r_idx: self.toggle_translation(table, row))
            table.setCellWidget(r_idx, 1, show_btn)

            play_btn = QPushButton("Play")
            play_btn.clicked.connect(lambda ch, text=item["word"]: self.play_audio(text))
            table.setCellWidget(r_idx, 2, play_btn)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Increase header height for clarity if needed
        table.horizontalHeader().setMinimumHeight(80)

        table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

        scroll_layout.addWidget(table)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Log attempt once viewed
        self.progress_tracker.log_attempt(self.lesson_id, "vocabulary", "viewed_vocab", True)

        continue_btn = QPushButton("Continue")
        continue_btn.setObjectName("continueButton")
        continue_btn.clicked.connect(self.on_complete)
        main_layout.addWidget(continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def toggle_translation(self, table, row):
        item = table.item(row, 0)
        data = item.data(Qt.ItemDataRole.UserRole)
        if data["isPolish"]:
            # Show English
            item.setText(data["english"])
            data["isPolish"] = False
            btn = table.cellWidget(row, 1)
            btn.setText("Show Polish")
        else:
            # Show Polish again
            item.setText(data["polish"])
            data["isPolish"] = True
            btn = table.cellWidget(row, 1)
            btn.setText("Show Translation")
        item.setData(Qt.ItemDataRole.UserRole, data)

    def play_audio(self, text):
        self.audio_manager.play_audio(text)
