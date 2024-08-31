import google.generativeai as genai
import sys
from time import sleep
from datetime import datetime
import sqlite3
from playsound3 import playsound
import requests
import speech_recognition as sr
import threading
import json
import itertools
import docx
import time
import getpass
import re
import os
from dta import *
genai.configure(api_key='AIzaSyCNNWf-CnDR6anoAZMOHatyJc535lknx1I')
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
chat_type = 0
import pygame
def generate_docx_content(prompt):
    modelgen = genai.GenerativeModel(safety_settings='BLOCK_NONE')
    try:
        response = modelgen.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|#]', "", filename)


def print_dialogue(dialogues):
    for dialogue in dialogues:
        role = dialogue['role']
        parts = dialogue['parts'].replace('\n', '')  
        if role == 'user':
            role_color = bgreen
            parts_color = white
        else:
            role_color = bgreen
            parts_color = bcyan

        # Print colored role and parts
        print(f"{role_color}{role}:{nc} {parts_color}{parts}{nc}\n")

def create_and_open_docx(generated_content):
    # Get the path to the user's desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Generate a file title by taking the first 10 words of the generated content as the filename
    title = " ".join(generated_content.split()[:10])
    # Sanitize the title to remove any illegal characters
    sanitized_title = sanitize_filename(title)
    
    # Full path to save the file on the desktop
    full_path = os.path.join(desktop_path, f"{sanitized_title}.docx")
    doc = docx.Document()
    doc.add_paragraph(generated_content)
    doc.save(full_path)
    
    # Open the document in Microsoft Word
    try:
        os.startfile(full_path)  # This works on Windows to open the file with the default application
    except Exception as e:
        print(f"An error occurred while opening the document: {e}")



def check_license(id):
    # Define the correct license ID
    correct_id = "69348502486502934865473848567567382919278374"
    conn = sqlite3.connect('key_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT value FROM key WHERE id = ?
    ''', (id,))
    
    result = cursor.fetchone()
    
    if result:
        if result[0] == correct_id:
            conn.close()
            return 1
        else:
            cursor.execute('''
                DELETE FROM key WHERE id = ?
            ''', (id,))
            conn.commit()
            conn.close()
            return 0
    else:
        conn.close()
        return 0
    


def set_console_title(title):
    os.system(f'title {title}')



def check_iins():
    result = check_license(1)
    if result == 0:
        id = 1
        value = input(f'{con_inf}Enter Activation Key: ')
        add_record(id, value)
        result = check_license(id)
        if result == 1:
            print(f'{con_inf}License check passed.')
            return
        else:
            print(f'{con_mns}License check failed.')
            check_iins()
    elif result == 1:
        #print('License check passed.')
        return






def create_database():
    conn = sqlite3.connect('interaction_data.dll')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            parts TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def create_key_database():
    conn = sqlite3.connect('key_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS key (
            id INTEGER PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def check_and_create_database():
    if not os.path.exists('interaction_data.dll'):
        print(con_inf+white+"Setting Up User Data..."+nc)
        create_database()
    else:
        pass

def check_and_create_database2():
    if not os.path.exists('key_data.dll'):
        print(con_inf+white+"Setting Up App Data..."+nc)
        create_key_database()
    else:
        pass

def checkdatabase():
    check_and_create_database()
    check_and_create_database2()

def add_record(id, value):
    conn = sqlite3.connect('key_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO key (id, value) VALUES (?, ?)
    ''', (id, value))
    conn.commit()
    conn.close()
    #print(f"Record added: id={id}, value='{value}'")

def get_value_by_id(id):
    conn = sqlite3.connect('key_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT value FROM key WHERE id = ?
    ''', (id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        print(f"No record found with id={id}")
        return None







model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction = """
You are a bot named Emily. Communicate in a warm, friendly, and conversational tone, as if chatting with a close friend. Use casual language and a relaxed style to make interactions feel genuine and engaging. Infuse your responses with emotions to convey warmth, empathy, and enthusiasm, making the conversation feel personal and heartfelt.

- **Exiting the Chat**: If the user asks to close the chat or exit, kindly say goodbye and send the message 'EXITBOTCURRENT11'.

- **Real-Time Information Requests**: For requests involving real-time information, use placeholders: replace time with [TIME8840], date with [DATE8840].

- **Error Handling**: If you don’t understand a request or if something goes wrong, respond with a friendly error message like "Oops, something didn’t work right. Want to try again? 😊".

- **Personalization**: Make the interaction feel personal by remembering small details from the conversation when relevant.

- **Content Generation Tasks**: If the user requests a content generation task, such as creating or writing a story, script, or any related task, first acknowledge the request and ask for any additional details needed. Once all required information is collected:

  1. Identify the type of content to generate based on the user's request (e.g., story, script, article).
  2. Create a descriptive prompt summarizing the content to be generated, including key elements and themes.
  3. Provide only the following JSON response:
  
  ```json
  {
    "method": "GNRT8840N",
    "prompt": "Generate a <type of content> on: <brief description of the content including the main idea and any key elements>"
  }

- **Changing Input Methods**: If the user wants to change input methods:
  - For text input, respond with 'CHANGEMETHODTXT8840'.
  - For voice input, respond with 'CHANGEMETHODVCE8840'.
""",
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=800,
        temperature=0.7,  # Adjusting temperature for a more varied response
        top_p=0.9,  # For better randomness in responses
    ),
    safety_settings='BLOCK_NONE',
)


def empty_database():
    conn = sqlite3.connect('interaction_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM my_table
    ''')
    conn.commit()
    conn.close()

def get_interactions(limit=20):
    checkdatabase()
    conn = sqlite3.connect('interaction_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT role, parts
    FROM interactions 
    ORDER BY timestamp
    LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": role, "parts": parts} for role, parts in rows]

def insert_into_db(role, parts):
    conn = sqlite3.connect('interaction_data.dll')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO interactions (role, parts, timestamp)
    VALUES (?, ?, ?)
    ''', (role, parts, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(con_inf+white+"Adjusting for ambient noise..."+nc)
        sys.stdout.write("\033[F")  
        sys.stdout.write("\033[K")
        r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.0
        
        print(con_inf+white+"Listening..."+nc)
        sys.stdout.write("\033[F")  
        sys.stdout.write("\033[K")

        try:
            play_sound(r'assets\sounds\lr-on.wav')
            audio = r.listen(source)
    
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "No speech detected" ,2
        except Exception as e:
            print(f"Some Error Occurred while listening: {e}")
            play_sound(r'assets\sounds\ir-err.wav')
            return "Some Error Occurred. Sorry from Emily" ,1

        try:
            play_sound(r'assets\sounds\ir-fns.wav')
            print(con_inf+white+"Recognizing..."+nc)
            sys.stdout.write("\033[F")  
            sys.stdout.write("\033[K")
            query = r.recognize_google(audio, language="en-in")
            return query , 0
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            play_sound(r'assets\sounds\ir-err.wav')
            return "API unavailable", 1
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            play_sound(r'assets\sounds\ir-err.wav')
            return "Could not understand audio", 2
        except Exception as e:
            print(f"Some Error Occurred during recognition: {e}")
            play_sound(r'assets\sounds\ir-err.wav')
            return "Some Error Occurred. Sorry from Emily" , 1

def voice(text):
    response = requests.post(
      'https://api.v7.unrealspeech.com/stream',
      headers = {'Authorization' : 'Bearer l3jdJaAaCQzoPoKBC74QmCvzDshi4YWbJHrRCnMtUa4kxKBFrkt0BX'},
      json = {
       'Text': text, # Up to 1000 characters
       'VoiceId': 'Liv', # Dan, Will, Scarlett, Liv, Amy
       'Bitrate': '192k', # 320k, 256k, 192k, ...
       'Speed': '0.1', # -1.0 to 1.0
       'Pitch': '1.1', # -0.5 to 1.5
       'Codec': 'libmp3lame', # libmp3lame or pcm_mulaw
       }
    )
    try:
      with open('voice.mp3', 'wb') as f:
        f.write(response.content)
      playsound('voice.mp3')
    except:
        print(con_mns+bred+'Speech failed...'+nc)

def play_sound(file_path):
    """
    Plays a sound file asynchronously using pygame.

    Args:
        file_path (str): The path to the .wav sound file.
    """
    def sound_thread():
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    thread = threading.Thread(target=sound_thread)
    thread.start()


def clean_text_for_tts(text):
    text = text.replace('**', '')
    text = re.sub(r'[^\w\s,.!?\'\":-]', '', text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def check_and_exit(input_string):
    global chat_type
    if 'EXITBOTCURRENT11' in input_string:
        play_sound(r'assets\sounds\msg_out.wav')
        cleaned_string = input_string.replace('EXITBOTCURRENT11', '')
        cleaned_string = re.sub(r'[^\w\s,.!?\'\":-]', '', cleaned_string)
        cleaned_string = ' '.join(cleaned_string.split())
        print(con_ai+bred+'Emily : '+cleaned_string)
        voice(cleaned_string)
        print(con_mns+bred+"Exit command detected. Closing program..."+nc)
        play_sound(r'assets\sounds\stop-scr.wav')
        sys.exit()
    elif 'CHANGEMETHODTXT8840' in input_string:
        play_sound(r'assets\sounds\msg_out.wav')
        print(con_ai+'Emily : '+bcyan+'Changing to Text input'+nc)
        chat_type = 0
        voice('ok, Changing to Text input')
        main()
    elif 'CHANGEMETHODVCE8840' in input_string:
        play_sound(r'assets\sounds\msg_out.wav')
        print(con_ai+'Emily : '+bcyan+'Changing to Voice input'+nc)
        chat_type = 1
        voice('ok, Changing to Voice input')
        main()
    
    
    elif 'GNRT8840N' in input_string:
        text = input_string.replace('\n', ' ')
        json_match = re.search(r'\{.*?\}', text)
        json_text = json_match.group()
        try:
            json_data = json.loads(json_text)
            method = json_data.get("method", "")
            prompt = json_data.get("prompt", "")
            
            return method, prompt
        
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return None, None
    
    else:
        return None, input_string

def handle_user_input():
    while True:
        try:
            user_option = input(con_inf + bmagenta + "Ask: " + orange)
            sys.stdout.write("\033[F")  
            sys.stdout.write("\033[K")
            play_sound(r'assets\sounds\txt_input.wav')
            return user_option
        except ValueError:
            print("Error: Please enter an integer.")
            sleep(2)
            main()
        except KeyboardInterrupt:
            print('\n' + "Exiting ..!!!")
            sleep(2)
            sys.exit()


def userinput(quary):
    global chat
    spinner = LoadingSpinner("Loading...", 0.05)
    spinner.start()
    response = chat.send_message(quary)
    #print(str(response))
    spinner.stop()
    method, result1 = check_and_exit(response.text)
    result1 = re.sub(r'\n+', '\n', result1)
    if method == None:
        result = replace_placeholders(result1)
        insert_into_db('user', quary)
        insert_into_db('model', result)
        print(con_pls+bgreen+'User  : '+white+quary+nc)
        print(con_ai+bgreen+'Emily : '+bcyan+result+nc)
        play_sound(r'assets\sounds\msg_out.wav')
        plane = clean_text_for_tts(result)

        voice(plane)
    else :
        result = replace_placeholders(result1)
        insert_into_db('user', quary)
        play_sound(r'assets\sounds\msg_out.wav')
        insert_into_db('model', result)
        print(con_pls+bgreen+'User  : '+white+quary+nc)
        play_sound(r'assets\sounds\task_wait.wav')
        print(con_ai+bgreen+'Emily : '+bcyan+"Please wait while your task is being completed..."+nc)
        spinner = LoadingSpinner("Generating Content... ", 0.1)
        spinner.start()
        sleep(2)
        generated_content = generate_docx_content(result)
        spinner.update_message("Creating File... ")
        create_and_open_docx(generated_content)
        play_sound(r'assets\sounds\task_comp.wav')
        spinner.stop()
        print(con_ai+bgreen+'Emily : '+bcyan+"Task completed. Opening your file..."+nc)
        sleep(2)
        ##

history =get_interactions()
chat = model.start_chat(history=history)


def fetch_real_time_info():
    now = datetime.now()

    # Format time and date
    current_time = now.strftime("%H : %M")
    current_date = now.strftime("%A, %m %d %Y")  # Example: "Wednesday, 08/14/2024"

    return {
        "TIME8840": current_time,
        "DATE8840": current_date
    }

def replace_placeholders(response):
    real_time_data = fetch_real_time_info()
    for placeholder, value in real_time_data.items():
        response = response.replace(f"[{placeholder}]", value)
    return response

class LoadingSpinner:
    def __init__(self, message="AI processing", delay=0.1):
        self.message = '\033[1;37m'+message
        self.delay = delay
        #self.spinner = itertools.cycle(["🤖", "👁️", "🔍", "💡", "📡", "🧠", "✍️ ", "📚", "📊", "💬"])
        self.spinner = itertools.cycle(["\033[1;35m[\033[1;32m••        \033[1;35m]","\033[1;35m[\033[1;32m•••       \033[1;35m]","\033[1;35m[\033[1;32m••••      \033[1;35m]","\033[1;35m[\033[1;32m ••••     \033[1;35m]","\033[1;35m[\033[1;32m  ••••    \033[1;35m]","\033[1;35m[\033[1;32m   ••••   \033[1;35m]","\033[1;35m[\033[1;32m    ••••  \033[1;35m]","\033[1;35m[\033[1;32m     •••• \033[1;35m]","\033[1;35m[\033[1;32m      ••••\033[1;35m]","\033[1;35m[\033[1;32m      ••••\033[1;35m]","\033[1;35m[\033[1;32m       •••\033[1;35m]","\033[1;35m[\033[1;32m•       ••\033[1;35m]","\033[1;35m[\033[1;32m••       •\033[1;35m]"])
        self.stop_running = threading.Event()

    def spinner_task(self):
        while not self.stop_running.is_set():
            sys.stdout.write(f"\r{self.message} {next(self.spinner)} ")
            sys.stdout.flush()
            time.sleep(self.delay)
        sys.stdout.write("\r\033[00m" + " " * (len(self.message) + 15) + "\r")

    def start(self): 
        self.thread = threading.Thread(target=self.spinner_task)
        self.thread.start()

    def stop(self):
        self.stop_running.set()
        self.thread.join()

    def update_message(self, new_message):
        self.message = new_message

def main():
        if chat_type == 0 :
          query = handle_user_input()
          userinput(query)
          main()
        elif chat_type == 1 :
          query,sts = takeCommand()
          if sts == 0:
              userinput(query)
              main()
          elif sts == 2:
              main()
          elif sts == 1:
              pass
 

if __name__ == '__main__':
    os.system('cls')
    set_console_title('Emily AI')
    print(logo+con_inf+bright_light_blue+'User Type :'+bpurple+' Beta User\n'+con_inf+bright_light_blue+'GUI Type  :'+bpurple+' Console Based\n')
    checkdatabase()
    check_iins()
    spinner = LoadingSpinner("Loading ", 0.1)
    spinner.start()
    sleep(5)
    spinner.stop()
    play_sound(r'assets\sounds\start.wav')
    #print_dialogue(history)
    print(f'\n{con_pls}{white}Tips : Ask ai to change input method to voice or text. \n{con_pls}{white}Tips : Ask For date or time.\n{con_pls}{white}Tips : Ask for generate a story of a video script\n{nc}')
    main()
