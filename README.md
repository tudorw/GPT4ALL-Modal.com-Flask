       ╔═══════════════════════════════════════════════╗
       ║                  Flask App                    ║
       ╚═══════════════════════════════════════════════╝
                                                      │
                                                      │ When the user enters the URL '/' in their web browser,
                                                      │ the Flask App receives the request and triggers the index()
                                                      │ function to handle the request. It prepares the homepage
                                                      │ by rendering an HTML template.
       ┌───────────────────────────────┴─────────────────┐
       │                   index()                        │ The index() function is responsible for handling the
       └───────────────────────────────┬─────────────────┘ homepage request. It renders the 'index.html' template,
                                                      │ which includes a form for the user to enter their question.
                                                      │
                                                      ▼ When the user submits the form on the homepage,
       ┌───────────────────────────────┴─────────────────┐ the Flask App receives a POST request to the
       │               ask_question()                       │ '/ask_question' URL. The ask_question() function
       └───────────────────────────────┬─────────────────┘ processes the user's question and generates a response.
                                                      │
                                                      ▼ Inside the ask_question() function, the data sent
       ┌───────────────────────────────┴─────────────────┐ by the user is extracted. This includes the
       │          Data Extraction                        │ question, model choices, number of runs, character
       └───────────────────────────────┬─────────────────┘ choice, and story arc choice. These values are
                                                      │ retrieved from the request and stored in variables
                                                      │ for further processing.
                                                      ▼ The Model Selection process determines which
       ┌───────────────────────────────┴─────────────────┐ conversation models to use for generating responses.
       │       Conversation History                      │ The conversation history keeps track of the
       └───────────────────────────────┬─────────────────┘ exchanged messages between the user and the AI
                                                      │ model. It stores the conversation history in a list,
                                                      │ allowing for context-aware responses.
         ┌───── while loop (num_runs) ──────────────────┐
         │                                               │ The code enters a while loop that iterates for the
         │    ┌─────────────────────────────────────┐    │ specified number of runs. This loop controls the
         │    │         Update scene ID             │    │ flow of the conversation exchanges.
         │    └─────────────────────────────────────┘    │
                                                      │
                                                      ▼ The Update scene ID process manages the current
         ┌─────────────────────────────────────┐         │ scene or section of the story. It updates the scene
         │         Update scene ID             │         │ ID, allowing the author to progress through the
         └─────────────────────────────────────┘         │ story in a structured manner.
                                                      │
                                                      ▼ The Get stage directions process retrieves the
         ┌─────────────────────────────────────┐         │ stage directions for the current scene. These
         │       Get stage directions          │         │ directions provide guidance to the author on how
         └─────────────────────────────────────┘         │ to write the scene, including actions, settings, and
                                                      │ other important details.
                                                      ▼ The Get scene instructions process retrieves the
         ┌─────────────────────────────────────┐         │ specific instructions for the current scene. These
         │     Get scene instructions          │         │ instructions provide guidance to the author on how
         └─────────────────────────────────────┘         │ to develop the scene, including plot points, character
                                                      │ interactions, and thematic elements.
                                                      ▼ The Get scene profile process retrieves the profile
         ┌─────────────────────────────────────┐         │ of the current scene. This profile includes information
         │        Get scene profile             │         │ such as the scene number, title, and other attributes
         └─────────────────────────────────────┘         │ that help guide the author's writing process.
                                                      │
                                                      ▼ The Generate scene content process generates the
         ┌─────────────────────────────────────┐         │ content for the current scene based on the provided
         │      Generate scene content         │         │ instructions, profile, and other relevant data.
         └─────────────────────────────────────┘         │ This content can include dialogues, descriptions,
                                                      │ and other elements necessary to develop the scene.
                                                      ▼ The Get antagonist profile process retrieves the
         ┌─────────────────────────────────────┐         │ profile of the antagonist character from a predefined
         │    Get antagonist profile           │         │ source. This profile describes the characteristics,
         └─────────────────────────────────────┘         │ traits, motivations, and role of the antagonist in
                                                      │ the story.
                                                      ▼ The Generate antagonist content process generates
         ┌─────────────────────────────────────┐         │ the content for the antagonist character based on
         │   Generate antagonist content       │         │ their profile. This content can include dialogues,
         └─────────────────────────────────────┘         │ actions, and other elements related to the antagonist's
                                                      │ role in the scene and overall story.
                                                      ▼ The Get protagonist profile process retrieves the
         ┌─────────────────────────────────────┐         │ profile of the protagonist character from a predefined
         │    Get protagonist profile          │         │ source. This profile describes the characteristics,
         └─────────────────────────────────────┘         │ traits, motivations, and role of the protagonist in
                                                      │ the story.
                                                      ▼ The Generate protagonist content process generates
         ┌─────────────────────────────────────┐         │ the content for the protagonist character based on
         │   Generate protagonist content      │         │ their profile. This content can include dialogues,
         └─────────────────────────────────────┘         │ actions, and other elements related to the protagonist's
                                                      │ role in the scene and overall story.
                                                      ▼ The Generate extras content process generates
         ┌─────────────────────────────────────┐         │ additional content for supporting characters or extras
         │    Generate extras content          │         │ in the scene. This content can include dialogues,
         └─────────────────────────────────────┘         │ actions, and other elements involving these characters.
                                                      ▼ The Update conversation history process adds the
         ┌─────────────────────────────────────┐         │ generated content and other exchanged messages to
         │  Update conversation history        │         │ the conversation history. This maintains a record
         └─────────────────────────────────────┘         │ of the entire conversation between the user and
                                                      │ the AI model, facilitating coherent storytelling.
                                                      ▼ The Generate summary process summarizes the
         ┌─────────────────────────────────────┐         │ current state of the conversation. It collects
         │        Generate summary             │         │ relevant information, such as the conversation
         └─────────────────────────────────────┘         │ history, generated content, and other details,
                                                      │ to create a concise summary of the ongoing story.
                                                      ▼ The while loop continues until the specified
                                                      │ number of runs is completed.


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
