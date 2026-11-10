import sys
import subprocess

def run_cmd(command):
        success = None
        failed = None
        code = None
        try: 
            output = subprocess.run(command, capture_output=True, text=True, check=True)
            success = output.stdout
            code = output.returncode
        except subprocess.CalledProcessError as e:
            failed = e.stderr
            code = e.returncode
        except FileNotFoundError:
            failed = f"Command '{command[0]}' not found"
            code = 127
        return success, failed, code
     

def display_output(command, success, failed, code):
    print(f"Command: {' '.join(command)}")
    print(f"Exit code: {code}")
    print(f"\n--- Output ---")
    if success:
        print(success)
    if failed:
        print(f"\n--- Errors ---")
        print(failed)

def main():
    if len(sys.argv) < 2:
        print("Error")
        print("Usage: python3 cmd_runner.py <command>")
        sys.exit(1)
    command = sys.argv[1:]
    success, failed, code = run_cmd(command)
    display_output(command, success, failed, code)

if __name__=="__main__":
    main()