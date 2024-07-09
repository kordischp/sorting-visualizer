import tkinter as tk
from tkinter import ttk
import random

# Global variables to store the generated array and delay time
generated_data = []
delay_time = 1

# Function to generate the array based on max value
def generate_array():
    max_value = int(max_entry.get())
    global generated_data
    generated_data = list(range(1, max_value))
    print(f"Generated Array: {generated_data}")
    draw_bars()

# Bubble sort algorithm with step-by-step yield
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                yield data

# Merge sort algorithm with step-by-step yield
def merge_sort(data, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(data, start, mid)
        yield from merge_sort(data, mid, end)

        left = data[start:mid]
        right = data[mid:end]

        i = j = 0
        for k in range(start, end):
            if i >= len(left):
                data[k] = right[j]
                j += 1
            elif j >= len(right):
                data[k] = left[i]
                i += 1
            elif left[i] < right[j]:
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1
            yield data

# Function to handle the run button click
def run_algorithm():
    selected_algorithm = algorithm_var.get()
    sorting_algorithm = globals()[selected_algorithm]
    if selected_algorithm == "merge_sort":
        sorting_generator = sorting_algorithm(generated_data, 0, len(generated_data))
    else:
        sorting_generator = sorting_algorithm(generated_data)
    animate_sort(sorting_generator)

# Function to animate the sorting process
def animate_sort(sorting_generator):
    try:
        next_data = next(sorting_generator)
        draw_bars()
        root.after(delay_time, lambda: animate_sort(sorting_generator))
    except StopIteration:
        return

# Function to update the delay time
def update_delay(value):
    global delay_time
    delay_time = int(value)
    print(f"Updated delay time: {delay_time} ms")

# Function to randomize the array
def randomize_array():
    global generated_data
    random.shuffle(generated_data)
    print(f"Randomized Array: {generated_data}")
    draw_bars()

# Function to reverse the array
def reverse_array():
    global generated_data
    generated_data.sort(reverse=True)
    print(f"Reversed Array: {generated_data}")
    draw_bars()

# Function to draw bars on the canvas
def draw_bars():
    canvas.delete("all")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    bar_width = canvas_width / len(generated_data)

    for i, value in enumerate(generated_data):
        x0 = i * bar_width
        y0 = canvas_height - (value / max(generated_data) * canvas_height)
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="")

# Create the main window
root = tk.Tk()
root.title("Algorithm Visualizer")
root.geometry("800x600")

# Create a frame for the view window
view_frame = tk.Frame(root, width=600, height=600, bg="dark grey")
view_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

# Create the canvas for visualization
canvas = tk.Canvas(view_frame, bg="dark grey")
canvas.pack(fill="both", expand=True)

# Create a frame for the settings
settings_frame = tk.Frame(root, width=200, height=600)
settings_frame.grid(row=0, column=1, sticky="n")

# Create and place the max value label and entry
max_label = tk.Label(settings_frame, text="Max Value:")
max_label.pack(pady=5)
max_entry = tk.Entry(settings_frame)
max_entry.pack(pady=5)

# Create and place the OK button
ok_button = tk.Button(settings_frame, text="OK", command=generate_array)
ok_button.pack(pady=5)

# Add a horizontal separator
separator1 = ttk.Separator(settings_frame, orient='horizontal')
separator1.pack(fill='x', pady=5)

# Create and place the sorting algorithm label
algorithm_label = tk.Label(settings_frame, text="Sorting Algorithm:")
algorithm_label.pack(pady=5)

# Create and place the algorithm selection dropdown
algorithm_var = tk.StringVar(settings_frame)
algorithm_var.set("bubble_sort")  # default value
algorithm_menu = tk.OptionMenu(settings_frame, algorithm_var, "bubble_sort", "merge_sort")
algorithm_menu.pack(pady=5)

# Add a horizontal separator
separator2 = ttk.Separator(settings_frame, orient='horizontal')
separator2.pack(fill='x', pady=5)

# Create and place the data type label
delay_label = tk.Label(settings_frame, text="Data type:")
delay_label.pack(pady=5)

# Create and place the randomize button
random_button = tk.Button(settings_frame, text="Random", command=randomize_array)
random_button.pack(pady=5)

# Create and place the reverse button
reverse_button = tk.Button(settings_frame, text="Reversed", command=reverse_array)
reverse_button.pack(pady=5)

# Add a horizontal separator
separator3 = ttk.Separator(settings_frame, orient='horizontal')
separator3.pack(fill='x', pady=5)

# Create and place the delay slider label
delay_label = tk.Label(settings_frame, text="Delay time (ms):")
delay_label.pack(pady=5)

# Create and place the delay slider
delay_slider = tk.Scale(settings_frame, from_=1, to=100, orient='horizontal', command=update_delay)
delay_slider.set(delay_time)  # set initial delay time
delay_slider.pack(pady=5)

# Add a horizontal separator
separator4 = ttk.Separator(settings_frame, orient='horizontal')
separator4.pack(fill='x', pady=5)

# Create and place the run button
run_button = tk.Button(settings_frame, text="Run", command=run_algorithm)
run_button.pack(pady=20)

# Configure the grid
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()
