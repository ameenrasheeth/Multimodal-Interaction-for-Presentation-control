import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import os
import convertapi


class PresentationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Presentation App")
        self.master.geometry("400x200")

        self.upload_button = tk.Button(self.master, text="Upload PowerPoint", command=self.upload_ppt)
        self.upload_button.pack(pady=10)

        self.hand_gesture_button = tk.Button(self.master, text="Hand Gesture Recognition", command=self.run_hand_gesture)
        self.hand_gesture_button.pack(pady=5)

        self.audio_recognition_button = tk.Button(self.master, text="Audio Recognition", command=self.run_audio_recognition)
        self.audio_recognition_button.pack(pady=5)

    def upload_ppt(self):
        filename = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx;*.ppt")])
        if filename:
            # Do something with the uploaded file, e.g., store its path
            self.ppt_path = filename
            print("Uploaded PowerPoint file:", filename)
            
            convertapi.api_secret = 'qDMtFwI4ejVFnr95'
            pptx_file_path = self.ppt_path
            output_folder_path = 'D:/Major/output_folder'
            for file_name in os.listdir(output_folder_path):
                file_path = os.path.join(output_folder_path, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            convertapi.convert('png', {'File': pptx_file_path}, from_format='ppt').save_files(output_folder_path)

    def run_hand_gesture(self):
        if hasattr(self, 'ppt_path'):
            # Assuming handgesture.py contains the code for hand gesture recognition
            # Replace 'handgesture.py' with the actual filename if different
            subprocess.Popen(['python', 'HandGesture.py', self.ppt_path])
        else:
            print("Please upload a PowerPoint file first.")

    def run_audio_recognition(self):
        if hasattr(self, 'ppt_path'):
            # Assuming audio.py contains the code for audio recognition
            # Replace 'audio.py' with the actual filename if different
            subprocess.Popen(['python', 'audio.py', self.ppt_path])
        else:
            print("Please upload a PowerPoint file first.")

def main():
    root = tk.Tk()
    app = PresentationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()