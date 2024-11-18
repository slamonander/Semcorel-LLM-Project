# Runs npm build, run, and start automatically for the frontend react

import subprocess
import os

# setting directory where frontend is located
frontend_directory = '/frontend/final'

# Function to run npm commands

def run_npm(command, cwd):
    try: 
        print(f"Running command: {command} in {cwd}, please wait.")
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True, capture_output=True)
        print(f"Output:\n{result.stdout}")

        if result.stderr:
            print(f"Error:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        print(f"Error Output: {e.stderr}")

def main():
    run_npm('npm install', 'final/frontend')
    run_npm('npm run build', 'final/frontend')
    run_npm('python app.py', 'final/backend') # Starts up the actual application
    # run_npm('npm start', 'final/frontend') # This starts up the testing React website

if __name__ == '__main__':
    main()
