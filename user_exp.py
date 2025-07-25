import os
import platform

def clear_screen():#Clears the terminal screen.
    # Check operating system to use the correct clear command
    if platform.system() == "Windows":
        os.system('cls')
    else: # For Linux and macOS
        os.system('clear')