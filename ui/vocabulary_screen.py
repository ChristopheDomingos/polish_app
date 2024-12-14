import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QWidgetItem, QFrame
from PyQt6.QtGui import QPixmap
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

        layout = QVBoxLayout()

        title = QLabel("Słownictwo (Vocabulary Introduction)")
        title.setObjectName("titleLabel")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        for item in self.vocab_data:
            row = QHBoxLayout()

            img_label = QLabel()
            if item.get("image") and os.path.exists(item["image"]):
                pix = QPixmap(item["image"]).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                img_label.setPixmap(pix)
            else:
                img_label.setText("[No Image]")

            word_label = QLabel(item['word'])
            # Create a translation label hidden initially
            translation_label = QLabel(item['translation'])
            translation_label.setVisible(False)

            show_translation_btn = QPushButton("Show Translation")
            show_translation_btn.clicked.connect(lambda _, lbl=translation_label: lbl.setVisible(True))

            play_btn = QPushButton("Play")
            play_btn.clicked.connect(lambda _, text=item["audio"], url=item.get("audio_url"): self.audio_manager.play_audio(text, url=url))

            row.addWidget(img_label)
            row.addWidget(word_label)
            row.addWidget(show_translation_btn)
            row.addWidget(translation_label)
            row.addWidget(play_btn)
            scroll_layout.addLayout(row)

        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # Not an exercise screen, but if you want to log attempts or score, you can skip. No attempts here.
        # Just when finishing viewing:
        self.progress_tracker.log_attempt(self.lesson_id, "vocabulary", "viewed_vocab", True)

        continue_btn = QPushButton("Continue")
        continue_btn.clicked.connect(self.on_complete)
        layout.addWidget(continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)