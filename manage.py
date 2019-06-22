
import sys
import os
import subprocess

argv = sys.argv

name = argv[0]
command = argv[1].lower()
helpmsg = """
        command: python3 manage.py {command}
        accept agruments: "build", "server", "rm-{file name}", "rm-all"
        e.g:
        - build and train data: python3 manage.py build
        - run server: python3 manage.py server
        - remove cache file: python3 manage.py rm-{file name} 
        - remove all cache data: python3 manage.py rm-all
        """
def main():
    if command == "help":
        print(helpmsg)
        return

    if command == "build":
        subprocess.check_output(["python3", "app/searcher/feature.py"])
        return

    if command == "server":
        subprocess.check_output(["python3", "app/searcher/index.py"])
        return

    if "rm" in command:
        filename = command[3:]
        if filename == "all":
            os.system("rm app/cache/*")
            return
        path = "app/cache/" + filename + ".pkl"
        os.system("rm " + path)
        return
    
    print("Invalid command.")
    print(helpmsg)

if __name__ == "__main__":
    # print(name, command)
    main()

