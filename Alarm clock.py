import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame
import os

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock with Focus Mode")
        self.root.geometry("400x400")
        self.root.config(bg="#f0f0f0")
        
        # Initialize pygame for sound
        pygame.mixer.init()

        # Set up the font style
        self.font = ("Helvetica", 14)

        # Header label
        self.header_label = tk.Label(root, text="Set Your Alarm", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.header_label.pack(pady=20)

        # Time input fields (for Hour, Minute, Second)
        self.time_frame = tk.Frame(root, bg="#f0f0f0")
        self.time_frame.pack(pady=10)

        self.hour_label = tk.Label(self.time_frame, text="Hour:", font=self.font, bg="#f0f0f0")
        self.hour_label.grid(row=0, column=0, padx=5)
        self.hour_entry = tk.Entry(self.time_frame, width=5, font=self.font)
        self.hour_entry.grid(row=0, column=1)

        self.minute_label = tk.Label(self.time_frame, text="Minute:", font=self.font, bg="#f0f0f0")
        self.minute_label.grid(row=0, column=2, padx=5)
        self.minute_entry = tk.Entry(self.time_frame, width=5, font=self.font)
        self.minute_entry.grid(row=0, column=3)

        self.second_label = tk.Label(self.time_frame, text="Second:", font=self.font, bg="#f0f0f0")
        self.second_label.grid(row=0, column=4, padx=5)
        self.second_entry = tk.Entry(self.time_frame, width=5, font=self.font)
        self.second_entry.grid(row=0, column=5)

        # Set alarm button
        self.set_alarm_button = tk.Button(root, text="Set Alarm", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=self.set_alarm)
        self.set_alarm_button.pack(pady=20)

        # Focus mode toggle button
        self.focus_mode = False
        self.focus_button = tk.Button(root, text="Enable Focus Mode", font=("Helvetica", 14), bg="#FF9800", fg="white", command=self.toggle_focus_mode)
        self.focus_button.pack(pady=10)

        # Display current time
        self.current_time_label = tk.Label(root, text="Current Time: ", font=("Helvetica", 14), bg="#f0f0f0")
        self.current_time_label.pack(pady=20)

        # Start a thread to update current time
        self.update_time()

        # Path to alarm sound file (change this path if needed)
        self.sound_file = "alarm_sound.wav"  # Ensure this file is in the same directory

    def update_time(self):
        # Get current time
        current_time = time.strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time}")
        
        # Update every second
        self.root.after(1000, self.update_time)
    
    def set_alarm(self):
        # Get alarm time from entries
        try:
            hour = int(self.hour_entry.get())
            minute = int(self.minute_entry.get())
            second = int(self.second_entry.get())
            self.alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"
            messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")
            
            # Start a thread to check if the alarm time is reached
            threading.Thread(target=self.check_alarm).start()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for time.")
    
    def check_alarm(self):
        while True:
            # Get the current time
            current_time = time.strftime("%H:%M:%S")
            if current_time == self.alarm_time:
                self.ring_alarm()
                break
            time.sleep(1)
    
    def ring_alarm(self):
        # Check if the sound file exists
        if not os.path.exists(self.sound_file):
            messagebox.showerror("File Not Found", f"The sound file '{self.sound_file}' was not found.")
            return
        
        # Play sound when the alarm goes off
        if not self.focus_mode:
            pygame.mixer.music.load(self.sound_file)  # Load the alarm sound file
            pygame.mixer.music.play(-1)  # Play sound infinitely
        if self.focus_mode:
            messagebox.showinfo("Focus Mode", "Focus mode is enabled. Alarm ringing silently.")
        else:
            messagebox.showinfo("Alarm", "Time's up!")

    def toggle_focus_mode(self):
        # Toggle focus mode
        self.focus_mode = not self.focus_mode
        if self.focus_mode:
            self.focus_button.config(text="Disable Focus Mode", bg="#F44336")
        else:
            self.focus_button.config(text="Enable Focus Mode", bg="#FF9800")


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    
    # Create an AlarmClock object
    alarm_clock = AlarmClock(root)
    
    # Run the main loop
    root.mainloop()
