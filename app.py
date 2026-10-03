from flask import Flask, render_template, abort
import yaml
import os

app = Flask(__name__)

# Die Punktwerte in der Reihenfolge, wie sie in der Tabelle erscheinen sollen
# Die erste Frage in der YAML-Liste bekommt den ersten Wert, etc.
POINT_VALUES = [20, 40, 60, 80, 100]

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@app.route('/')
def index():
    config = load_config()
    topics = config.get('topics', [])

    # Wir fügen jedem Thema eine ID hinzu, damit wir sie in der URL verwenden können
    for idx, topic in enumerate(topics):
        topic['id'] = idx

    return render_template('index.html', topics=topics, point_values=POINT_VALUES)

@app.route('/question/<int:topic_id>/<int:point>')
def question(topic_id, point):
    config = load_config()
    topics = config.get('topics', [])

    if topic_id < 0 or topic_id >= len(topics):
        abort(404)

    topic = topics[topic_id]

    # Finde heraus, an welcher Stelle der Punktwert in POINT_VALUES steht
    try:
        question_index = POINT_VALUES.index(point)
    except ValueError:
        abort(404)

    # Prüfe, ob für dieses Thema genug Fragen in der YAML existieren
    if question_index >= len(topic.get('questions', [])):
        abort(404)

    question_data = topic['questions'][question_index]

    return render_template(
        'question.html', 
        topic_id=topic_id, 
        topic_name=topic['name'], 
        point=point, 
        question_text=question_data['question']
    )

@app.route('/answer/<int:topic_id>/<int:point>')
def answer(topic_id, point):
    config = load_config()
    topics = config.get('topics', [])

    if topic_id < 0 or topic_id >= len(topics):
        abort(404)

    topic = topics[topic_id]

    try:
        question_index = POINT_VALUES.index(point)
    except ValueError:
        abort(404)

    if question_index >= len(topic.get('questions', [])):
        abort(404)

    answer_data = topic['questions'][question_index]

    return render_template(
        'answer.html', 
        topic_name=topic['name'], 
        point=point, 
        answer_text=answer_data['answer']
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)

