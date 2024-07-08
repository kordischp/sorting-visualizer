import tkinter as tk
import algorithms

# Function to handle the run button click
def run_algorithm():
    min_value = int(min_entry.get())
    max_value = int(max_entry.get())
    data = list(range(min_value, max_value + 1))

    selected_algorithm = algorithm_var.get()
    module = getattr(algorithms, selected_algorithm)
    sorted_data = getattr(module, selected_algorithm)(data)
    #sorted_data = sort_function(data)
    
    print(f"Sorted Data: {sorted_data}")

# Create the main window
root = tk.Tk()
root.title("Algorithm Visualizer")
root.geometry("800x600")

# Create a frame for the view window
view_frame = tk.Frame(root, width=600, height=600, bg="white")
view_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

# Create a frame for the settings
settings_frame = tk.Frame(root, width=200, height=500)
settings_frame.grid(row=0, column=1, sticky="n")

# Create and place the min value label and entry
min_label = tk.Label(settings_frame, text="Min Value:")
min_label.pack(pady=5)
min_entry = tk.Entry(settings_frame)
min_entry.pack(pady=5)

# Create and place the max value label and entry
max_label = tk.Label(settings_frame, text="Max Value:")
max_label.pack(pady=5)
max_entry = tk.Entry(settings_frame)
max_entry.pack(pady=5)

# Create and place the sorting algorithm label
algorithm_label = tk.Label(settings_frame, text="Sorting Algorithm:")
algorithm_label.pack(pady=5)

# Create and place the algorithm selection dropdown
algorithm_var = tk.StringVar(settings_frame)
algorithm_var.set("bubble_sort")  # default value
algorithm_menu = tk.OptionMenu(settings_frame, algorithm_var, "bubble_sort", "merge_sort")
algorithm_menu.pack(pady=5)

# Create and place the run button
run_button = tk.Button(settings_frame, text="Run", command=run_algorithm)
run_button.pack(pady=20)

# Configure the grid
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()

