from flask import Flask, request, jsonify, render_template
import modal
import os
from gpt4all import GPT4All as GPT4AllModule
import datetime
import yaml

def download_model(model_choice):
    import gpt4all
    return gpt4all.GPT4All(model_choice)

image = modal.Image.debian_slim().pip_install("gpt4all").run_function(download_model)
stub = modal.Stub("gpt4all", image=image)

@stub.cls(keep_warm=1)
class GPT4All:
    def __init__(self, model_name, stub):
        self.model_name = model_name
        self.stub = stub

    def __enter__(self):
        self.gptj = GPT4AllModule(self.model_name)
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
    character_choice = data['character_choice']
    story_arc_choice = data['story_arc_choice']
    conversation_history = []
    exchange_count = 0
    is_first_question = True

    while exchange_count < num_runs:

        if exchange_count > 1 :
            is_first_question=False
            conversation_prompt=' '.join(conversation_history)
        else:
            conversation_prompt = (character_choice + ' ' + question + ' '.join(conversation_history))         
            conversation_history.append(question)
            #storyArc is set in form, load the helping material and use that to aid the story writer
            with open('static/data/arc/' + story_arc_choice + '/arc.yml', 'r') as file:
                content = file.read()
            content = content.replace('\n', ' ')
            conversation_history_joined = ' '.join(conversation_history)
            arc_profile_prompt= ('The story we are writing uses the '+ story_arc_choice +' here is the story so far, please work out where we are in the arc and set the stage for the next scene ' + conversation_history_joined)
            arc_profile = get_answer_from_model(model_choice_2,  arc_profile_prompt)
            # set and store the storyArc name into a new file to edit and load for the next run

        
        
        #output story meta for user to see and save to disk

        writers_instructions = arc_profile + " is the story arc type chosen for this story, please write a novel with 50-60 scenes, where 25% of the scenes are for the Beginning Hook, 50% for the Middle Build, and 25% for the Ending Payoff.\n\nWrite a compelling story that follows the structure of a traditional novel, consisting of three main parts: the beginning, the middle, and the end. Your goal is to create a unique and captivating narrative within the range of 800 to 1000 words, enough for one episode of the story.\n\nBreak down your novel into scenes, which are the building blocks of your story. Remember that scenes are where the writer's craft shines, so focus on crafting impactful and engaging scenes. Aim for approximately 20 words per scene, treating each scene as a small movement along the arc.\n\nTo start, allocate 1 or 2 scenes for the essential elements of your story: the inciting incidents, progressive complications, crisis questions, climaxes, and resolutions for the beginning, middle, and end.\n\nFor the remaining scenes, distribute them as follows: 25% for the Beginning, 50% for the Middle, and 25% for the End. This breakdown will provide you with a rough guide on the number of scenes needed in each section.\n\nWhile this structure provides a helpful framework, keep in mind that there are no rigid rules about the exact number of scenes. Feel free to adjust the scene distribution as needed to suit your story. The primary objective is to map out a manageable path to complete your first draft. Once you reach the end, you can revise and refine the scenes to create a polished final episode."
              
            
        # get profile from yaml
        with open('static/data/characters/Raquel/profile.yml', 'r') as file:
            content = file.read()
        content = content.replace('\n', ' ')

        antagonist_yaml_profile_prompt= ('Take the following YAML and return a short but emotional charged plain english description of the individual and their traits.' + content)
        antagonist_profile = get_answer_from_model(model_choice_2, antagonist_yaml_profile_prompt)

        # Antagonist
        conversation_prompt1= (conversation_prompt + ':is the story so far. Here is a profile of the character in the story that I want you to act as; ' + antagonist_profile + '. Review the story so far, provided. So what would you say and do next? Please reply with only story content and dialogue. ')
        answer_1 = get_answer_from_model(model_choice_1, conversation_prompt1)
        # Protagnist
       
        with open('static/data/characters/Raquel/profile.yml', 'r') as file:
            content = file.read()
        content = content.replace('\n', ' ')
        protagonist_profile_prompt= ('Take the following YAML and return a short but emotional charged plain english description of the individual and their traits.' + content)
        protagonist_profile = get_answer_from_model(model_choice_2, protagonist_profile_prompt)
        # Add the answer to the conversation history
        conversation_history.append(answer_1)
        conversation_prompt2= (conversation_prompt + answer_1 + ': Here is a profile of the character that I want you to act as;' + protagonist_profile + '. So what would you say and do next? Please reply with only story content and dialogue.')

        answer_2 = get_answer_from_model(model_choice_1, conversation_prompt2)
        # Protagnist
        conversation_history.append(answer_2)

        # randomly bring in extras here, and cameos even more rarely

       # Sunmmarise
        conversation_prompt3= (' '.join(conversation_history)+ writers_instructions)
        answer_3 = get_answer_from_model(model_choice_2, conversation_prompt3) 

        # Add the answer to the conversation history or should we replace? then todo, load the storyARc yaml and use the template story arc yaml to create a new storyArc yaml with the story so far
        conversation_history.append(answer_3)
        exchange_count += 1        
        # todo iterate through raquel.yml and use llm to update each sections value only 

        # todo, get feedback from llm of users contribution and check it fits existing story line and make reccomendations

        # thread names properly

        ## process in parallel where it makes sense

        #choose or set a story arc based on first question, then maintain the yaml storyarc documents in stories/

    return jsonify({'conversation_history': conversation_history})
    

def get_answer_from_model(model_choice, conversation_prompt):
    
    with GPT4All(model_choice, stub) as model:
        completion = model.generate(conversation_prompt)
        answer_content = completion['choices'][0]['message']['content']
    return answer_content

if __name__ == '__main__':
    app.run(debug=True)