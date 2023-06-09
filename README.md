Summary:

Classes:
Flask App: Handles the Flask application and routes.
Functions:
index(): Renders the 'index.html' template for the homepage.
ask_question(): Processes the user's question and generates a response.
Data Extraction: Extracts data from the user's input.
Model Selection: Determines the conversation models to use.
Conversation History: Tracks the exchanged messages.
Update scene ID: Manages the current scene or section of the story.
Get stage directions: Retrieves the stage directions for the scene.
Get scene instructions: Retrieves specific instructions for the scene.
Get scene profile: Retrieves the profile of the current scene.
Generate scene content: Generates content for the current scene.
Get antagonist profile: Retrieves the profile of the antagonist character.
Generate antagonist content: Generates content for the antagonist character.
Get protagonist profile: Retrieves the profile of the protagonist character.
Generate protagonist content: Generates content for the protagonist character.
Generate extras content: Generates additional content involving supporting characters or extras.
Update conversation history: Adds generated content to the conversation history.
Generate summary: Creates a summary of the conversation and story.
Variables:
model_choice_1, model_choice_2: Choices for the conversation models.
num_runs: Number of conversation exchanges to perform.
character_choice: Choice of the character for the story.
story_arc_choice: Choice of the story arc.
conversation_history: Keeps track of the conversation history.
exchange_count: Tracks the number of conversation exchanges.
Constants:
'/': URL route for the homepage.
'/ask_question': URL route for processing the question.
User Input:
Question: Entered by the user through the homepage form.
Arrays:
N/A
Output:
JSON response with the generated conversation history.
