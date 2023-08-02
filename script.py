import random
import speech_recognition as sr
import requests
import webbrowser
# Import other libraries as needed for task management and weather APIs


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return None



def analyze_intent(text, api_key):
    api_url = "https://language.googleapis.com/v1/documents:analyzeEntities"
    headers = {"Content-Type": "application/json"}
    payload = {
        "document": {"type": "PLAIN_TEXT", "content": text},
        "encodingType": "UTF8",
    }
    params = {"key": api_key}

    response = requests.post(api_url, headers=headers, json=payload, params=params)
    data = response.json()

    if "entities" in data:
        return data["entities"]
    else:
        return []



# Function to retrieve weather information
def get_current_weather(api_key, location):
        """
        Returns the current temperature and conditions for the given location using the weatherapi.com API.

        Parameters:
            api_key (str): The API key for weatherapi.com.
            location (str): The location to get the weather for.

        Returns:
            A tuple containing the current temperature and conditions (in that order).
        """
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        temp_f = data["current"]["temp_f"]
        conditions = data["current"]["condition"]["text"]
        name = data['location']['name']

        return(f"The current temperature in {name} is {temp_f} degrees Fahrenheit with {conditions} conditions.")

# Function to exit program
def exit_program():
    message = ['Goodbye!', 'See you later!', 'Bye bye!', 'Have a great day!', 'Adios!', 'Bye for now!']
    print(random.choice(message))
    exit()

# Make a task structure and system
class Task:
    def __init__(self, description, priority="medium", due_date=None, tags=None, notes=None, status = 'incomplete'):
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.tags = tags if tags else []
        self.notes = notes if notes else []
        self.completed = False

    def mark_completed(self):
        self.completed = True
        
    def set_status(self, status):
         self.status = status

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_note(self, note):
        self.notes.append(note)

    def __str__(self):
        return f"{self.description} (Priority: {self.priority}, Due Date: {self.due_date}, Tags: {self.tags}, Notes: {self.notes}, Completed: {self.completed})"

tasks = []
def add_task(task_description):
     # Remove the phrase "to the to-do list" if present in the task description
    task_description = task_description.replace("to the to-do list", "").strip()
    tasks.append(task_description)

def view_tasks():
    if not tasks:
        return "The to-do list is empty."
    else:
        return "Here are the tasks on your to-do list:\n" + "\n".join(tasks)

# Process the user query to identify the intent and take appropriate actions.
def process_query(query):
    # User/Stuart interactions
     if "hello" in query or 'hi' in query:
         return 'Hi there!'
     if 'bye' in query or 'goodbye' in query:
         return exit_program()
     if 'who are you' in query or 'what is your name' in query or 'what can you do' in query:
         return "My name is S.T.U.A.R.T! I am here to help."   
     
    # Web Promptings
     if 'Google' in query:
         return webbrowser.open('http://google.com')
     if 'GPT' in query:
         return webbrowser.open('https://chat.openai.com/')
     if 'YouTube' in query:
         return webbrowser.open('http://google.com')
     
     
     # Tasks Management and Organization
     if "add" in query:
        # Extract the task description (e.g., "add buy groceries to the to-do list")
        task_description = query.replace("add", "").strip()
        add_task(task_description)
        return "Task added to the to-do list."
     if "tasks" in query or "to-do list" in query:
        return view_tasks()
    
    # Weather
     if "weather" in query:
        words = query.split()  # Split the query into words
        # Look for the word "weather" and get the location from the word following it
        index = words.index("weather")
        location = " ".join(words[index+2:]).strip()
        #location = query.replace("weather", "").strip()
        
        try:
            weather_api_key = "16a843261eaa4eb19d720800230208"
            return get_current_weather(weather_api_key, location)
        except Exception as e:
            return "Sorry, I couldn't get that. Please try again."

        
    # Math Equations
     if "solve" in query:
        # Extract the math expression (e.g., "1 + 1")
        math_expr = query.replace("solve", "").strip()

        try:
            # Evaluate the math expression
            result = eval(math_expr)
            return f"The result of {math_expr} is {result}"
        except Exception as e:
            return "Sorry, I couldn't evaluate the expression. Please try again."

   
    # Add more condition checks and actions for other types of queries as needed.

     return "I'm not sure how to assist with that. Please try another query."

# Handling user input and querying for response
def virtual_assistant(api_key):
    print("Virtual Assistant: How can I assist you?")
    while True:
        user_input = speech_to_text()
        if user_input is not None:
            # Process the user query
            response = process_query(user_input)
            print(response)

            # Implement responses to other queries based on the processing logic.
            # For example, you can add tasks to the to-do list, get weather forecasts, etc.


# 'Main' function 
if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with the actual API key for the Google Cloud Natural Language API
    api_key = "AIzaSyB2qVlLOc5hYJQHK1906ce98rqzJDUtfLg"
    virtual_assistant(api_key)
