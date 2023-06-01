from flask import Flask, request, jsonify, render_template
import modal
import gpt4all

image = modal.Image.debian_slim().pip_install("gpt4all").pip_install("flask").pip_install("pyyaml")
stub = modal.Stub("gpt4all", image=image)

@stub.cls(keep_warm=1)
class GPT4All:
    def __init__(self, model_name):
        self.model_name = model_name

    def __enter__(self):
        print("Downloading model")
        self.gptj = gpt4all.GPT4All(self.model_name)
        print("Loaded model")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @modal.method()
    def generate(self, question):
        messages = [{"role": "user", "content": question}]
        completion = self.gptj.chat_completion(messages)
        return completion

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question_from_request = data.get('question')
    num_runs = int(data.get('num_runs', 1))
    character_choice = data.get('character_choice', 'A Helpful Person')
    answers = []
    with GPT4All(data.get('model_choice')) as model:  # Pass the model name as an argument
        for _ in range(num_runs):
            question = character_choice + ' ' + question_from_request
            answer = model.generate(question)
            answers.append(answer)

    return jsonify({'answers': answers})

if __name__ == '__main__':
    app.run(debug=True)