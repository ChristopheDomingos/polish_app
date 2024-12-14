import json
import os
from datetime import datetime

class ProgressTracker:
    def __init__(self, filename="data/progress_data.json"):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"attempts": []}, f, ensure_ascii=False, indent=2)
        self.filename = filename

    def log_attempt(self, lesson_id, exercise_type, question, correct):
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data["attempts"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "lesson_id": lesson_id,
            "exercise_type": exercise_type,
            "question": question,
            "correct": correct
        })
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)