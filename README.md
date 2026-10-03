# Der Große Preis

A minimalist web application for the group game "Der Große Preis".

## Quick Start

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Create `config.yaml`**
   ```bash
   cp config-example.yaml config.yaml
   # Adjust config as needed
   ```
3. **Run the server:**
   ```bash
   python app.py
   ```
4. **Open in browser:** http://127.0.0.1:5000

## Configuration
Edit `config.yaml` to add your own categories and questions. The point values are automatically assigned based on the order of questions in the YAML list.

## Keyboard Shortcuts
- **`{Cat ID}` > `{Point ID}`**: Select a question (e.g., `1` then `2` for the first category, 40 points).
- **`A`**: Reveal the answer.
- **`H`**: Return to the main overview (home).

## Features
- **Progress Tracking:** Answered questions are dimmed and locked via browser cookies.
- **Legible Design:** Clean, centered layout for use on large screens or projectors.
- **No-JS Fallback:** Fully navigable via mouse clicks.
