from flask import Flask, render_template, abort, request, make_response
import yaml
import waitress

app = Flask(__name__)
POINT_VALUES = [20, 40, 60, 80, 100]

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Hilfsfunktion zum Parsen der Cookies
def get_answered_questions():
    answered_cookie = request.cookies.get('answered_questions', '')
    # Cookie Format: "0-20,0-40,1-20"
    return answered_cookie.split('_') if answered_cookie else []

@app.route('/')
def index():
    topics = config.get('topics', [])
    for idx, topic in enumerate(topics):
        topic['id'] = idx

    answered = get_answered_questions()
    return render_template('index.html', topics=topics, point_values=POINT_VALUES, answered=answered)

@app.route('/question/<int:topic_id>/<int:point>')
def question(topic_id, point):
    config = load_config()
    topics = config.get('topics', [])
    if topic_id < 0 or topic_id >= len(topics): abort(404)
    topic = topics[topic_id]
    try:
        question_index = POINT_VALUES.index(point)
    except ValueError: abort(404)
    if question_index >= len(topic.get('questions', [])): abort(404)

    question_data = topic['questions'][question_index]
    return render_template('question.html', topic_id=topic_id, topic_name=topic['name'], point=point, question_text=question_data['question'])

@app.route('/answer/<int:topic_id>/<int:point>')
def answer(topic_id, point):
    config = load_config()
    topics = config.get('topics', [])
    if topic_id < 0 or topic_id >= len(topics): abort(404)
    topic = topics[topic_id]
    try:
        question_index = POINT_VALUES.index(point)
    except ValueError: abort(404)
    if question_index >= len(topic.get('questions', [])): abort(404)

    question_data = topic['questions'][question_index]

    # Cookie Logik: Aktuelle Frage hinzufügen
    answered = get_answered_questions()
    item = f"{topic_id}-{point}"
    if item not in answered:
        answered.append(item)

    resp = make_response(render_template(
        'answer.html', 
        topic_name=topic['name'], 
        point=point, 
        question_text=question_data['question'], 
        answer_text=question_data['answer']
    ))

    # Cookie speichern (gültig für 30 Tage)
    resp.set_cookie('answered_questions', '_'.join(answered), max_age=60*60*24*30)
    return resp

if __name__ == '__main__':
    config = load_config()
    waitress.serve(app, port=5000)

