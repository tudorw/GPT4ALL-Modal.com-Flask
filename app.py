from flask import Flask, request, jsonify, render_template
import modal
import os
from gpt4all import GPT4All as GPT4AllModule
import datetime
import yaml
import re

def extract_number(value):
    # Search for the first number in the string
    match = re.search(r'\d+(\.\d+)?', value)
    if match:
        # If a number is found, return it as an integer
        return int(float(match.group()))
    else:
         # If no number is found, return None or maybe pass off to ai for another guess...todo
        return None
    
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
    scene_id=0
    
    while exchange_count < num_runs:
        # if scene number is set increment by 1 unless it is equal to the highest scene number in /Overcoming The Monsters/arc.yml if it is then mark the story as complete and return, else continue

        # on first question, prepend question
        if exchange_count > 1 :
            is_first_question=False
            conversation_prompt=' '.join(conversation_history)
            print("Logging to console")
            #check scene number against arc, if scene number = max scene number in arc, write file to /generated with a unique filename and pin to ipfs, then choose the next arc from arc folder and continue
            
        else:
          
            conversation_prompt = (question + ' '.join(conversation_history))         
            conversation_history.append(question)

        #storyArc is set in form, load the helping material and use that to aid the story writer
        #with open('static/data/arc/' + story_arc_choice + '/arc.yml', 'r') as file:
        #    content = file.read()
        #arc = content.replace('\n', ' ')
        conversation_history_joined = ' '.join(conversation_history)
        
        # get stage direction
        with open('static/data/arc/' + story_arc_choice + '/stage_directions.yml', 'r') as file:
            content = file.read()
        stage_direction = content.replace('\n', ' ')

        #working, skip for now to speed up testing, todo remove comments #
            #get example text
            #with open('static/data/arc/' + story_arc_choice + '/simple_example.txt', 'r') as file:
            #    content = file.read()
            #example = content.replace('\n', ' ')
        # arc_profile_prompt= ('Return to me just one scene number from  "'+ arc +'" that best matches this text " ' + conversation_history_joined +' "  take your best guess, it does not matter if you are wrong, if you fail, return the number 1, take care to return a number and only a number, no text, or comment on the number of around the number, a computer will read the number and will error if it is supplied with any text.')
        # arc_profile = get_answer_from_model(model_choice_2,  arc_profile_prompt)
        # # use the previous prompt result, first check it is a number and number only!
        # scene_id = extract_number(arc_profile)
        # if scene_id is None:
        #     scene_id = 1
        
        # todo does arc_profile=number, is number in stage directions, if not, get the ai to try again...
        # use stage directions to get scene_instructions
        #get scene information from stage_directions.yml
        #get example text
        scene_id += 1   
        #scene_instructions_prompt= (character_choice +' Please read Scene Number ' + str(scene_id) + ' in this yaml  "' + stage_direction +'" use the Introduction, props, cast members and artifacts to write a single scene.  Only return one scene, content, no small talk or comment on output. or mention of scene or other instructions or context.' )
        with open('static/data/arc/' + story_arc_choice + '/stage_directions.yml', 'r') as file:
            stage_directions_yaml = file.read()
        scene_text = re.search(fr'Scene {scene_id}(.*?)(?=Scene {scene_id + 1})', stage_directions_yaml, re.DOTALL)
        if scene_text:
         scene_text = scene_text.group(1).strip()
        else:
         scene_text = f"The scene {scene_id}."
        
        # check how long conversation history is, if over context limit then summarise 4,000 tokens (approximately 3,000 words), let's limit it to 1000 words 20 minutes	2,000 words
        #In general script format, usually one page equals one minute. Though it does depend on the variant. If you're calling out every single shot (as is more common in animation, though a number of cartoons actually make the storyboards and then write the scripts), that changes it. And I believe some comedies have their dialogue double-spaced, which changes things also.
        # #But with the normal script format, each episode would be about 22 pages, as they're about 22 minutes.
        conversation_history_word_count = sum(len(sentence.split()) for sentence in conversation_history_joined)
        if conversation_history_word_count > 1000:
         summary_prompt = "Please summarize the following text to approximately 1000 words: " + conversation_history_joined
         conversation_history_joined_summary = get_answer_from_model(model_choice_2, summary_prompt)
         conversation_history_joined = conversation_history_joined_summary

        # use the conversation history, or summarised conversation history to get the directions for the next scene
        scene_instructions_prompt = (character_choice + ' The context for this scene is "'+ conversation_history_joined +'". Now Please use that together with the following information to write a single scene: "' + scene_text + '". Only return the written content, no small talk or comment on output. or mention of scene or other instructions or context.')
        
        scene_instructions = get_answer_from_model(model_choice_1,  scene_instructions_prompt)
            # set and store the storyArc name into a new file to edit and load for the next run

        # run once casting agent, review arc and find cast, then match cast needed to cast available in /cast
        # run once location finder, review arc and match with locations
        # given the script arc.yml, please identify how many cast members are required and titile their roles, then use this list /cast of available actors and select the roles from that list, output a yaml code block with the results.
        # store the scene number and increment it on each run
        # use scene_isntructions to direct author(character choice) after collecting yaml info on author style
        #output story meta for user to see and save to disk
        # timeline_manager, read this story and check that it is consistent and well aligned with timeline.yaml
        # continuity, please compare this scene with the previous scene and suggest relevant change to help them align more closely
        # soundtrack
        # sfx
        # visuals
        # text to speeach, brian or...


        #writers_instructions = arc_profile + " is the story arc type chosen for this story, please write a novel with 50-60 scenes, where 25% of the scenes are for the Beginning Hook, 50% for the Middle Build, and 25% for the Ending Payoff.\n\nWrite a compelling story that follows the structure of a traditional novel, consisting of three main parts: the beginning, the middle, and the end. Your goal is to create a unique and captivating narrative within the range of 800 to 1000 words, enough for one episode of the story.\n\nBreak down your novel into scenes, which are the building blocks of your story. Remember that scenes are where the writer's craft shines, so focus on crafting impactful and engaging scenes. Aim for approximately 20 words per scene, treating each scene as a small movement along the arc.\n\nTo start, allocate 1 or 2 scenes for the essential elements of your story: the inciting incidents, progressive complications, crisis questions, climaxes, and resolutions for the beginning, middle, and end.\n\nFor the remaining scenes, distribute them as follows: 25% for the Beginning, 50% for the Middle, and 25% for the End. This breakdown will provide you with a rough guide on the number of scenes needed in each section.\n\nWhile this structure provides a helpful framework, keep in mind that there are no rigid rules about the exact number of scenes. Feel free to adjust the scene distribution as needed to suit your story. The primary objective is to map out a manageable path to complete your first draft. Once you reach the end, you can revise and refine the scenes to create a polished final episode."
        writers_instructions = 'The story so far "'.join(conversation_history) +'". These are the scene instructions for the next part of the story "'+ scene_instructions_prompt +'" ' + character_choice + '" and return the text for the scene including use of props, artifacts, scenes, sound, visuals, and dialog for the cast: '
         
        # Sunmmarise
        answer_3 = get_answer_from_model(model_choice_2, writers_instructions) 

        # Add the answer to the conversation history or should we replace? then todo, load the storyARc yaml and use the template story arc yaml to create a new storyArc yaml with the story so far
        conversation_history.append(answer_3)
        # get profile from yaml
        with open('static/data/cast/Raquel/profile.yml', 'r') as file:
            content = file.read()
        content = content.replace('\n', ' ')

        antagonist_yaml_profile_prompt= ('Take the following YAML and return a 30 word emotionally charged plain english description of the individual and their traits.' + content)
        #antagonist_profile = get_answer_from_model(model_choice_2, antagonist_yaml_profile_prompt)
        antagonist_profile = 'I am the antagonist.'

        # Antagonist
        conversation_prompt1= (conversation_history_joined + ':is the story so far. "' + antagonist_profile + '". Review the story so far, provided. So what would you say and do next? Please reply with only story content and dialogue. ')
        answer_1 = get_answer_from_model(model_choice_1, conversation_prompt1)
        # Protagnist
       
        with open('static/data/cast/ZebraZero/profile.yml', 'r') as file:
            content = file.read()
        content = content.replace('\n', ' ')
        protagonist_profile_prompt= ('Take the following YAML and return a 30 word but emotionally charged plain english description of the individual and their traits.' + content)
        #protagonist_profile = get_answer_from_model(model_choice_2, protagonist_profile_prompt)
        protagonist_profile = 'I am the protagonist.'
        # Add the answer to the conversation history
        conversation_history.append(answer_1)
        conversation_prompt2= (conversation_history_joined + answer_1 + ':is the story so far.  "' +  protagonist_profile + '". So what would you say and do next? Please reply with only story content and dialogue.')

        answer_2 = get_answer_from_model(model_choice_1, conversation_prompt2)
        # Protagnist
        conversation_history.append(answer_2)

        # randomly bring in extras here, and cameos even more rarely

       
        exchange_count += 1        
        # summarise and write the current conversation to a yaml and create a 'story so far' summary and update conversation history
        # Write conversation history to a new yaml file in data/generated
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"static/generated/{story_arc_choice}_{timestamp}.yaml"

        with open(filename, 'w') as file:
            yaml.dump(conversation_history, file)

        
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