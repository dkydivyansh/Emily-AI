import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

# Global variables
cap = cv2.VideoCapture(0)
running = True

# Function to show the video feed using Tkinter's after() method
def update_frame():
    if running:
        ret, frame = cap.read()
        if ret:
            # Convert the frame to an image Tkinter can display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update video label
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)
        
        # Call this function again after 10ms to update the frame
        video_label.after(10, update_frame)

# Create the main window
root = tk.Tk()
root.title("Chatbot App")
root.geometry("800x600")  # Adjusted the window size for better layout
root.resizable(False, False)

# Create a Notebook widget for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create the chatbot tab
chatbot_frame = ttk.Frame(notebook, width=600, height=400)
chatbot_frame.pack(fill="both", expand=True)

# Chat Display
chat_display = tk.Text(chatbot_frame, height=20, width=70, state='disabled', bg="#f0f0f0", wrap="word")
chat_display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Add File Button
add_file_button = ttk.Button(chatbot_frame, text="Add File", width=10)
add_file_button.grid(row=1, column=0, padx=10, pady=10)

# Message Entry
message_entry = ttk.Entry(chatbot_frame, width=40)
message_entry.grid(row=1, column=1, padx=10, pady=10)

# Send Button
send_button = ttk.Button(chatbot_frame, text="Send", width=10)
send_button.grid(row=1, column=2, padx=5, pady=10)

# Switch to Speech Button
speech_button = ttk.Button(chatbot_frame, text="Switch to Speech", width=15)
speech_button.grid(row=1, column=3, padx=5, pady=10)

# Add chatbot tab to notebook
notebook.add(chatbot_frame, text='Chatbot')

# Create the video tab
video_frame = ttk.Frame(notebook, width=600, height=400)
video_frame.pack(fill="both", expand=True)

# Create a label for displaying video feed
video_label = ttk.Label(video_frame)
video_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Input box in video tab
video_input = ttk.Entry(video_frame, width=40)
video_input.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Ask Button
ask_button = ttk.Button(video_frame, text="Ask", width=10)
ask_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

# Add video tab to notebook
notebook.add(video_frame, text='Video Feed')

# Start the video feed using after method
update_frame()

# Start the main event loop
root.mainloop()

# Release the capture and destroy OpenCV windows when the program ends
cap.release()
cv2.destroyAllWindows()
