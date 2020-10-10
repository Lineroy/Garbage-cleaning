import ctypes
import os

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


if is_admin() != 0:

    repositories = [os.environ["TMP"], r"C\Windows\Temp"]

    operation = input("Delete files?(Y, N): ").upper()

    without_possibility = []

    if operation.startswith("Y" or "Д"):
        while len(repositories) != 0:
            while True:
                for path, dirs, files in os.walk(repositories[0]):
                    for remove_files in files:
                        try:
                            os.remove(os.path.join(path, remove_files))
                            print(f"Removing... {remove_files}")
                        except PermissionError:
                            without_possibility.append(remove_files)
                            os.system(f'DEL /Q /S /F {os.path.join(path, remove_files)}')
                            continue
                    for remove_dirs in dirs:
                        try:
                            os.rmdir(os.path.join(path, remove_dirs))
                            print(f"Removing... {remove_dirs}")
                        except OSError:
                            without_possibility.append(remove_dirs)
                            os.system(f'rd /Q /S {os.path.join(path, remove_dirs)}')
                            continue

                repositories.remove(repositories[0])

                break

    else:
        exit()

    print("\nFiles or folders that cannot be deleted due to internal factors: ")
    print("; ".join(without_possibility))

else:
    print("You have opened the program without administrator rights, please try again!")
    non_command = input()
