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
    question = data['question']
    model_choice_1 = data['model_choice_1']
    model_choice_2 = data['model_choice_2']
    num_runs = int(data['num_runs']) 
   

    conversation_history = [question]

    for i in range(num_runs):
        # Model 1 answers
        answer_1 = get_answer_from_model(model_choice_1, conversation_history)
        conversation_history.append(answer_1)

        # Model 2 answers
        answer_2 = get_answer_from_model(model_choice_2, conversation_history)
        conversation_history.append(answer_2)

    return jsonify({'conversation_history': conversation_history})


def get_answer_from_model(model_choice, conversation_history):
    with GPT4All(model_choice) as model:
        prompt = ' '.join(conversation_history) 
        completion = model.generate(prompt)
        answer_content = completion['choices'][0]['message']['content']
    return answer_content

if __name__ == '__main__':
    app.run(debug=True)
