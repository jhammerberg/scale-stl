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
from madcad import *

def prompt_scale():
    print(colored("Scaling options:", attrs=["bold"]))
    print(colored("A - inches to millimeters (input*25.4)", "light_blue"))
    print(colored("B - millimeters to inches (input/25.4)", "light_blue"))
    print(colored("%<percent> - scale by any percent value (e.g. %150 => 150%)", "light_blue"))
    print(colored("*<coefficient> - scale by any coefficient (e.g. *2 => double size)", "light_blue"))
    user_input = input(colored("Command: ", "blue")).strip()
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
    input_file = input(colored("Path to STL file: ", color="blue"))
    output_file = input(colored("Path to scaled output STL file: ", color="blue"))
    try:
        part = read(input_file)
    except Exception:
        print(colored("Could not parse input STL file, bad path or bad file format. Press enter to exit.", color="red", attrs=["bold"]))
        input()
        exit(0)
    scale = prompt_scale()
    transformed = part.transform(mat3(scale))
    try:
        write(transformed, output_file)
    except Exception:
        print(colored("Could not write to specified output, probably bad file path. Press enter to exit.", color="red", attrs=["bold"]))
        input()
        exit(0)
    

if __name__ == "__main__":
    main()
    print(colored("File scaled! Press enter to exit.", color="green"))
    input()
    exit(0)
