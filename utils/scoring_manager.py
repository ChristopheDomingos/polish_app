# scoring_manager.py
class ScoringManager:
    def __init__(self):
        self.score = 0
        self.total_possible = 0
        self.difficult_exercises = set()

    def add_exercise(self, points=10):
        # Each exercise adds to the total possible points
        self.total_possible += points

    def correct_answer(self, first_try=True):
        # For example:
        # If first try correct: full points (10)
        # If second try correct: slightly fewer points (7)
        if first_try:
            self.score += 10
        else:
            self.score += 7

    def wrong_answer(self, final_attempt=False, exercise_id=None):
        # No points for wrong attempts.
        # If final attempt wrong, mark as difficult
        if final_attempt and exercise_id:
            self.difficult_exercises.add(exercise_id)

    def get_score(self):
        return self.score

    def get_total_possible(self):
        return self.total_possible

    def get_difficult_exercises(self):
        return self.difficult_exercises
