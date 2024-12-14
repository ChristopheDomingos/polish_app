# lesson_loader.py
import json
import random
import unicodedata

class LessonLoader:
    def __init__(self, lesson_file):
        with open(lesson_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_overview(self):
        return self.data.get("overview", {})

    def get_grammar_insight(self):
        return self.data.get("grammar_insight", {})

    def get_vocabulary(self):
        return self.data.get("vocabulary", [])

    def get_exercises(self, category):
        exercises = self.data.get(category, [])
        if len(exercises) > 5:
            return random.sample(exercises, 5)
        return exercises

    def get_guided_practice(self):
        return self.get_exercises("guided_practice")

    def get_writing_practice(self):
        return self.get_exercises("writing_practice")

    def get_listening_and_speaking(self):
        return self.get_exercises("listening_and_speaking")

    def get_real_life_dialogue(self):
        dialogue_data = self.data.get("real_life_dialogue", {})
        all_ex = dialogue_data.get("interactive_choices", [])
        if len(all_ex) > 5:
            choices = random.sample(all_ex, 5)
        else:
            choices = all_ex
        return dialogue_data.get("dialogue", []), choices

    def get_mini_quiz(self):
        return self.get_exercises("mini_quiz")

    def get_review_feedback(self):
        return self.data.get("review_and_feedback", {})

    @staticmethod
    def normalize_text(text):
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        text = ''.join(replacements.get(char, char) for char in text)
        text = unicodedata.normalize('NFD', text)
        text = ''.join(ch for ch in text if not unicodedata.combining(ch))
        # Keep only alphanumeric and spaces
        text = ''.join(ch for ch in text if ch.isalnum() or ch.isspace())
        return ' '.join(text.lower().split())

    @staticmethod
    def check_answer(user_answer, correct_answers):
        # correct_answers is a list of valid answers
        user_norm = LessonLoader.normalize_text(user_answer)
        for ans in correct_answers:
            ans_norm = LessonLoader.normalize_text(ans)
            if user_norm == ans_norm:
                return True
        return False
