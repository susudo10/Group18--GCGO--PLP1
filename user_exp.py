import os
import platform

def clear_screen():#Clears the terminal screen.
    if platform.system() == "Windows":
        os.system('cls')
    else: # For Linux and macOS
        os.system('clear')