import tkinter as tk
from tkinter import ttk
import threading
import queue

# Create a queue to communicate with the data-sending thread
data_queue = queue.Queue()

# Create the main window
window = tk.Tk()
window.title("ESP8266 12-Servo Control Interface")
window.geometry("420x650")  # Set window size

# Create a frame for the scrollbar
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas for the scrollable area
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas and bind it to the scroll events
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas
frame_inside_canvas = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_inside_canvas, anchor="nw")

# Store angle and speed values for 12 servos
servo_angle_vars = [tk.IntVar(value=90) for _ in range(12)]  # Default angle = 90
servo_speed_vars = [tk.IntVar(value=5) for _ in range(12)]   # Default speed = 5

# Create UI components for each servo inside the scrollable frame
for i in range(12):
    # Create a LabelFrame for each servo
    servo_frame = ttk.Labelframe(frame_inside_canvas, text=f"Servo {i+1} Controls", padding=(10, 5))
    servo_frame.pack(fill=tk.BOTH, padx=10, pady=5)

    # Create angle slider
    angle_label = ttk.Label(servo_frame, text="Angle:")
    angle_label.grid(row=0, column=0, padx=5, pady=5)
    angle_slider = ttk.Scale(servo_frame, from_=0, to=180, variable=servo_angle_vars[i], orient='horizontal', length=250)
    angle_slider.grid(row=0, column=1, padx=5, pady=5)

    # Create speed slider
    speed_label = ttk.Label(servo_frame, text="Speed (1=Fast, 10=Slow):")
    speed_label.grid(row=1, column=0, padx=5, pady=5)
    speed_slider = ttk.Scale(servo_frame, from_=1, to=10, variable=servo_speed_vars[i], orient='horizontal', length=250)
    speed_slider.grid(row=1, column=1, padx=5, pady=5)

# Function to send data from UI to the sending script through a queue
def send_data():
    while True:
        # Put current slider values in the queue
        angles = [angle.get() for angle in servo_angle_vars]
        speeds = [speed.get() for speed in servo_speed_vars]
        data_queue.put((angles, speeds))
        window.after(100)  # Repeat every 100 ms

# Start the data-sending thread
thread = threading.Thread(target=send_data)
thread.daemon = True
thread.start()

# Run the main loop
window.mainloop()
