# grammar_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QWidget as QW, QFrame
)
from PyQt6.QtCore import Qt

class GrammarScreen(QWidget):
    def __init__(self, grammar_data, on_complete):
        super().__init__()
        self.grammar_data = grammar_data
        self.on_complete = on_complete

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title (No inline style, rely on style.qss)
        title = QLabel("Grammar Insight")
        title.setObjectName("titleLabel")
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        explanation_text = self.grammar_data.get("explanation", "")
        explanation_label = QLabel(explanation_text)
        explanation_label.setObjectName("explanationLabel")
        explanation_label.setWordWrap(True)
        main_layout.addWidget(explanation_label)

        # Scroll area for tables if they overflow
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QW()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(20)

        # Add tables without extra titles
        for table_data in self.grammar_data.get("tables", []):
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])

            table_widget = QTableWidget()
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(rows))

            for r_idx, row_data in enumerate(rows):
                for c_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    table_widget.setItem(r_idx, c_idx, item)

            # Resize to fit content
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table_widget.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
            table_widget.setFrameShape(QFrame.Shape.Panel)
            table_widget.setFrameShadow(QFrame.Shadow.Raised)

            scroll_layout.addWidget(table_widget)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # No "Play Grammar Explanation" button anymore

        continue_btn = QPushButton("Continue")
        continue_btn.setObjectName("continueButton")
        continue_btn.clicked.connect(self.on_complete)
        main_layout.addWidget(continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
