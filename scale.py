# /// script
# requires-python = "==3.12"
# dependencies = [
#     "colored",
#     "numpy-stl",
#     "pymadcad",
#     "yaspin",
# ]
# ///

from termcolor import colored
from yaspin import yaspin
spinner = yaspin()
spinner.text = colored("Initializing...", "yellow")
spinner.start()
import madcad
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

def print_dimensions(part):
    mesh = part.box()
    min_coords = mesh.min
    max_coords = mesh.max
    width = round(max_coords.x - min_coords.x, 3)
    depth = round(max_coords.y - min_coords.y, 3)
    height = round(max_coords.z - min_coords.z, 3)
    print(colored(f"> Width={width}", "light_blue"))
    print(colored(f"> Depth={depth}", "light_blue"))
    print(colored(f"> Height={height}", "light_blue"))

def input_path():
    root.attributes('-topmost', True)

    file_path = filedialog.askopenfilename(
        initialdir=".",
        title="Select a file",
        filetypes=(("Mesh file", "*.stl"), ("All files", "*.*"))
    )

    root.attributes('-topmost', False)
    if file_path:
        return file_path
    else:
        exit(0)

def save_path():
    root.attributes('-topmost', True)

    file_path = filedialog.asksaveasfilename(
        defaultextension=".stl",
        initialfile="output.stl",
        filetypes=[("Mesh file", "*.stl"), ("All files", "*.*")],
        title="Save File As"
    )

    root.attributes('-topmost', False)
    if file_path:
        return file_path
    else:
        exit(0)

def prompt_scale():
    print(colored("Scaling options:", attrs=["bold"]))
    print(colored("A - inches to millimeters (input*25.4)", "light_blue"))
    print(colored("B - millimeters to inches (input/25.4)", "light_blue"))
    print(colored("%<percent> - scale by any percent value (e.g. %150 => 150%)", "light_blue"))
    print(colored("*<coefficient> - scale by any coefficient (e.g. *2 => double size)", "light_blue"))
    user_input = input(colored("> ", "cyan")).strip().capitalize()
    if ("A" in user_input):
        return 25.4
    elif ("B" in user_input):
        return 1 / 25.4
    elif (user_input.startswith("%")):
        try:
            percent = float(user_input[1:])
            return percent / 100.0
        except ValueError:
            print(colored("INVALID PERCENT: " + user_input, color="red", attrs=["bold"]))
            return prompt_scale()
    elif user_input.startswith("*"):
        try:
            scale = float(user_input[1:])
            return scale
        except ValueError:
            print(colored("INVALID SCALE: " + user_input, color="red", attrs=["bold"]))
            return prompt_scale()
    else:
        print(colored("INVALID OPTION: " + user_input, color="red", attrs=["bold"]))
        return prompt_scale()


def main():
    spinner.stop()
    print(colored("Use the dialoge box to select input file.", "blue"))
    input_file = input_path()
    try:
        part = madcad.read(input_file)
    except Exception:
        print(colored("Could not parse input STL file, bad path or bad file format. Press enter to exit.", color="red", attrs=["bold"]))
        input()
        exit(0)
    print(colored("File found! Initial dimensions:", "green"))
    print_dimensions(part)
    try_again = True
    while (try_again):
        print("--------------------------------")
        scale = prompt_scale()
        transformed = part.transform(madcad.mat3(scale))
        print(colored("Part scaled! New dimensions:", "green"))
        print_dimensions(transformed)
        answer = input(colored("Do these dimensions look right? (Y/N): ","cyan")).strip().capitalize()
        if ((answer == "Y") or (answer == "YES")):
            try_again = False
        elif ((answer == "N") or (answer == "NO")):
            try_again = True
        else:
            print(colored("Invalid input, answer Y or N. Try again.",color="red",attrs=["bold"]))
    print(colored("Use the dialoge box to save the scaled STL file.", "blue"))
    output_file = save_path()
    try:
        madcad.write(transformed, output_file)
    except Exception:
        print(colored("Could not write to specified output, probably bad file path. Press enter to exit.", color="red", attrs=["bold"]))
        input()
        exit(0)
    print(colored("File saved! Press enter to scale another file or close this window to exit.", color="green"))
    input()
    

if __name__ == "__main__":
    while True:
        main()
