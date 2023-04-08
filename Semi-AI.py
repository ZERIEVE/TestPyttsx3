import speech_recognition as sr 
import webbrowser, wikipedia, datetime, pyttsx3
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the pre-trained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Initialize the text-to-speech engine
engine = pyttsx3.init() #initialize an instance

# Define a function to speak a given text
def speak(text):

    voice = engine.getProperty('voices') #get the available voices
    engine.setProperty('voice', voice[1].id) #changing voice to index 1 for female voice
    engine.say(text)
    engine.runAndWait()

# Define a function to recognize speech
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"You: {query}\n")
    except Exception as e:
        print("I'm sorry, I didn't understand that.")
        query = None
    return query

# Define a function to generate a response to a given input
def generate_response(user_input, max_length=25):
    # Encode the input text
    input_ids = tokenizer.encode(user_input, return_tensors='pt')

    # Generate a response using the GPT-2 model
    output_ids = model.generate(input_ids, max_length=max_length, do_sample=True)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return output_text

# Greet the user
hour = datetime.datetime.now().hour
if hour >= 0 and hour < 12:
    speak("Good morning!")
elif hour >= 12 and hour < 18:
    speak("Good afternoon!")
else:
    speak("Good evening!")
speak("I am Zerieve . How can I assist you today?")

# Loop to receive user input and respond
while True:
    # Get user input
    user_input = recognize_speech()

    # Check for exit command
    if user_input is None or "exit" in user_input.lower():
        speak("Goodbye!")
        break

    # Respond to user input
    if "wikipedia" in user_input.lower():
        speak("Searching Wikipedia...")
        query = user_input.lower().replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia,")
        speak(results)
    elif "open youtube" in user_input.lower():
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com/")
    elif "open google" in user_input.lower():
        speak("Opening Google...")
        webbrowser.open("https://www.google.com/")
    elif "play music" in user_input.lower():
        speak("Playing music...")
        webbrowser.open("https://music.youtube.com/")
    elif "what time is it" in user_input.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "what is the date" in user_input.lower():
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"The current date is {current_date}")
    else:
        response  = generate_response(user_input)
        speak(response)

    # Ask for more input
    speak("Is there anything else I can assist you with?")

