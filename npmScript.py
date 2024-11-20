# Runs npm build, run, and start automatically for the frontend react

import subprocess
import atexit # Will automate the cleanup function to terminate npm start process

npm_process = None


# The cleanup function for termination
def cleanup():
    global npm_process
    if npm_process and npm_process.poll() is None: # Checks if process is still running
        print ("Stopping npm start process, please wait...")
        npm_process.terminate()

atexit.register(cleanup)

# Function to run npm commands

def run_npm(command, cwd, wait=True):
    try: 
        print(f"Running command: {command} in {cwd}, please wait.")

        if wait:
            result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True, capture_output=True)
            print(f"Output:\n{result.stdout}")
            if result.stderr:
                print(f"Error:\n{result.stderr}")
        else:
            process = subprocess.Popen(command, shell=True, cwd=cwd)
            print(f"Process started: {process.pid} (use this PID to terminate if needed)")
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        print(f"Error Output: {e.stderr}")

def main():
    run_npm('npm install', 'final/frontend')
    run_npm('npm run build', 'final/frontend')
    # run_npm('python app.py', 'final/backend') # Starts up the actual application
    run_npm('npm start', 'final/frontend', wait=False) # Runs in the background

if __name__ == '__main__':
    main()
