import tkinter as tk
from tkinter import ttk
import random
import winsound
import threading

# Global variables to store the generated array and delay time
generated_data = []
delay_time = 1

# Function to generate the array based on max value
def generate_array():
    try:
        max_value = int(max_entry.get())
        if not 3 <= max_value <= 1000:
            max_value = 100
            max_entry.delete(0, tk.END)
            max_entry.insert(0, str(max_value))
    except ValueError:
        max_value = 100
        max_entry.delete(0, tk.END)
        max_entry.insert(0, str(max_value))

    global generated_data
    generated_data = list(range(1, max_value + 1))  # Include max_value in the list
    print(f"Generated Array: {generated_data}")
    draw_bars()

# Bubble sort algorithm with step-by-step yield
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            yield data, j, j + 1  # Yield the data and the indices being compared
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                yield data, j, j + 1  # Yield again after the swap

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
            yield data, start + i if i < len(left) else start + j, mid + j if j < len(right) else mid + i
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
            yield data, k, k  # Yield again after placing the element

# Selection sort algorithm with step-by-step yield
def selection_sort(data):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield data, min_idx, j  # Yield the data and the indices being compared
            if data[j] < data[min_idx]:
                min_idx = j
                yield data, min_idx, j  # Yield again when a new minimum is found
        data[i], data[min_idx] = data[min_idx], data[i]
        yield data, i, min_idx  # Yield after the swap

# Insertion sort algorithm with step-by-step yield
def insertion_sort(data):
    n = len(data)
    for i in range(1, n):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            yield data, j, j + 1  # Yield the data and the indices being compared
            data[j + 1] = data[j]
            j -= 1
            yield data, j, j + 1  # Yield again after the swap
        data[j + 1] = key
        yield data, j + 1, i  # Yield after placing the key

# Gnome sort algorithm with step-by-step yield
def gnome_sort(data):
    index = 0
    n = len(data)
    while index < n:
        if index == 0:
            index += 1
        if data[index] >= data[index - 1]:
            index += 1
        else:
            data[index], data[index - 1] = data[index - 1], data[index]
            yield data, index, index - 1  # Yield the data and the indices being compared
            index -= 1

# Cocktail shaker sort algorithm with step-by-step yield
def cocktail_shaker_sort(data):
    n = len(data)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            yield data, i, i + 1  # Yield the data and the indices being compared
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                swapped = True
                yield data, i, i + 1  # Yield again after the swap
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            yield data, i, i + 1  # Yield the data and the indices being compared
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                swapped = True
                yield data, i, i + 1  # Yield again after the swap
        start += 1

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
        next_data, index1, index2 = next(sorting_generator)
        threading.Thread(target=play_sound, args=(generated_data[index1], generated_data[index2])).start()
        draw_bars(index1, index2)
        root.after(delay_time, lambda: animate_sort(sorting_generator))
    except StopIteration:
        draw_bars()  # Draw final state with no highlighted bars

# Function to play sound based on bar values
def play_sound(value1, value2):
    def get_frequency(value):
        min_freq = 120
        max_freq = 1212
        min_value = min(generated_data)
        max_value = max(generated_data)
        return min_freq + (value - min_value) * (max_freq - min_value) / (max_value - min_value)

    freq1 = get_frequency(value1)
    freq2 = get_frequency(value2)
    duration = 200  # Duration for audible sound in milliseconds

    # Play two frequencies consecutively
    winsound.Beep(int(freq1), duration)
    winsound.Beep(int(freq2), duration)

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

# Function to reset the program to its original state
def reset_program():
    global generated_data
    generated_data = []
    max_entry.delete(0, tk.END)
    draw_bars()
    print("Program has been reset")

# Function to draw bars on the canvas
def draw_bars(index1=None, index2=None):
    canvas.delete("all")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    if generated_data:
        bar_width = canvas_width / len(generated_data)
    else:
        bar_width = canvas_width

    for i, value in enumerate(generated_data):
        x0 = i * bar_width
        y0 = canvas_height - (value / max(generated_data) * canvas_height)
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        color = "red" if i == index1 or i == index2 else "white"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

# Create the main window
root = tk.Tk()
root.title("Algorithm Visualizer")
root.geometry("800x600")

# Configure the grid layout
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

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
max_label = tk.Label(settings_frame, text="Max Value (3-1000):")
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
algorithm_menu = tk.OptionMenu(settings_frame, algorithm_var, "bubble_sort", "merge_sort", "selection_sort", "insertion_sort", "gnome_sort", "cocktail_shaker_sort")
algorithm_menu.pack(pady=5)

# Add a horizontal separator
separator2 = ttk.Separator(settings_frame, orient='horizontal')
separator2.pack(fill='x', pady=5)

# Create and place the data type label
delay_label = tk.Label(settings_frame, text="Data type:")
delay_label.pack(pady=5)

# Create a frame for the randomize and reverse buttons
button_frame = tk.Frame(settings_frame)
button_frame.pack(pady=5)

# Create and place the randomize button in the button frame
random_button = tk.Button(button_frame, text="Random", command=randomize_array)
random_button.grid(row=0, column=0, padx=5)

# Create and place the reverse button in the button frame
reverse_button = tk.Button(button_frame, text="Reversed", command=reverse_array)
reverse_button.grid(row=0, column=1, padx=5)

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
run_button.pack(pady=5)

# Add a horizontal separator
separator5 = ttk.Separator(settings_frame, orient='horizontal')
separator5.pack(fill='x', pady=5)

# Create and place the reset button
reset_button = tk.Button(settings_frame, text="Reset", command=reset_program)
reset_button.pack(pady=5)

# Start the Tkinter main loop
root.mainloop()
