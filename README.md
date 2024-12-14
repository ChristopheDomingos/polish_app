# Polish Lessons App

This application helps you learn Polish through a structured approach:

- **Welcome & Lesson Selection**: Start with a welcome screen to choose which lesson to attempt.
- **Grammar Insight First**: Introduces grammar before vocabulary and exercises.
- **Vocabulary Section**: Introduces words with on-demand translation and audio.
- **Guided Practice, Writing, Listening & Speaking, Real-Life Dialogue, Mini Quiz**:
  - Each offers randomized exercises (5 chosen each session from a pool of 20).
  - Two attempts per exercise: first fail gives a hint, second fail reveals answer and marks exercise as difficult.
  - Multiple correct answers supported.
  - Normalization of input so no Polish keyboard is required.
  - Translation available on demand via a toggle button.
  - Scoring system: correct first try = full points, second try = fewer points, failure = no points.
- **Review & Feedback**: Final score displayed, recommendations given. Difficult exercises are tracked for repetition.

## How to Run

1. `pip install -r requirements.txt`
2. `python main.py`

## Directory Structure
(See directory structure listed above.)

## Customization
Modify `lesson_1.json` to add more exercises, translations, hints, etc.

## Future Improvements
- Add more lessons in `lessons/`.
- Integrate better spaced repetition using `progress_tracker` data.
