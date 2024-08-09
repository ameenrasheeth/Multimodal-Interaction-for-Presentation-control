import os
import cv2
import numpy as np
import pyaudio
import json
import vosk
import time
from word2number import w2n 

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "D:\Major\output_folder"

# Initialize Vosk speech recognition
model_path = "D:\\Major\\vosk-model-en-in-0.5"
vosk.SetLogLevel(-1)
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, 16000)

# Variables
imgNumber = 0
buttonPressed = False
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

# Function to recognize speech from audio input
def recognize_speech():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    print("Listening...")

    start_time = time.time()  # Record the start time

    while time.time() - start_time < 3:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_json = json.loads(result)
            if 'text' in result_json:
                command = result_json['text'].lower()
                print("Command:", command)
                process_voice_command(command)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to process voice commands
def process_voice_command(command):
    global imgNumber
    global buttonPressed

    if "next" in command:
        if imgNumber + 1 < len(pathImages):
            imgNumber += 1
            buttonPressed = True
            print("Going to next slide")
        else:
            print("Already on the last slide")
    
    elif "previous" in command:
        if imgNumber - 1 >= 0:
            imgNumber -= 1
            buttonPressed = True
            print("Going to previous slide")
        else:
            print("Already on the first slide")
    
    elif "go to" in command or "goto":
        # Extract the word representation of the slide number from the command
        slide_number_words = command.split()[-1]
        
        try:
            # Convert word representation of the number to its numeric value
            slide_number = w2n.word_to_num(slide_number_words)
            
            # Check if the slide number is within the range of available slides
            if 0 <= slide_number - 1 < len(pathImages):
                imgNumber = slide_number - 1  # Adjust to zero-based indexing
                buttonPressed = True
                print("Navigating to slide", slide_number)
            else:
                print("Slide number out of range.")
        except ValueError:
            print("Invalid slide number format.")

   

# Main loop
while True:
    # Get image frame
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    fixed_size = (800, 600) 
    imgCurrent = cv2.resize(imgCurrent, fixed_size)

    cv2.imshow("Slide", imgCurrent)

    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break

    # Call function to recognize speech commands
    recognize_speech()

cv2.destroyAllWindows()
