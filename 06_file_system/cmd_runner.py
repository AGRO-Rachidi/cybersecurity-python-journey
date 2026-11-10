import sys
import subprocess

def run_cmd(command):
        success = None
        failed = None
        code = None
        try: 
            # On récupère la sortie sans l'afficher tout de suite, pour la présenter ensuite.
            output = subprocess.run(command, capture_output=True, text=True, check=True)
            success = output.stdout
            code = output.returncode
        except subprocess.CalledProcessError as e:
            # Avec check=True, une commande qui échoue arrive ici avec son code de retour.
            failed = e.stderr
            code = e.returncode
        except FileNotFoundError:
            # Ce cas arrive notamment si le nom de la commande n'existe pas sur la machine.
            failed = f"Command '{command[0]}' not found"
            code = 127
        # On renvoie les deux sorties possibles et le code, même quand la commande échoue.
        return success, failed, code
     

def display_output(command, success, failed, code):
    # On garde un petit résumé avant d'afficher ce que la commande a renvoyé.
    print(f"Command: {' '.join(command)}")
    print(f"Exit code: {code}")
    print(f"\n--- Output ---")
    if success:
        print(success)
    if failed:
        print(f"\n--- Errors ---")
        print(failed)

def main():
    # Tout ce qui suit le nom du script est transmis comme commande à exécuter.
    if len(sys.argv) < 2:
        print("Error")
        print("Usage: python3 cmd_runner.py <command>")
        sys.exit(1)
    command = sys.argv[1:]
    success, failed, code = run_cmd(command)
    display_output(command, success, failed, code)

if __name__=="__main__":
    main()