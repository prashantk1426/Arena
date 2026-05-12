import os
import subprocess
import sys

def package():
    print("--- ARENA STANDALONE PACKAGING TOOL ---")
    
    # Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define the command
    # --onefile: Create a single exe
    # --noconsole: Don't show terminal window
    # --name: Name of the output file
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name", "ArenaArcade",
        "--clean",
        "main.py"
    ]

    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("\nSUCCESS!")
        print("Your standalone executable is located in the 'dist' folder.")
        print("File: dist/ArenaArcade.exe")
    except Exception as e:
        print(f"\nFAILED: {e}")

if __name__ == "__main__":
    package()
