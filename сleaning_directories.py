import ctypes
import os


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


if is_admin() != 0:

    repositories = [os.environ["TMP"], r"C\Windows\Temp"]

    question = input("Do you want to add a cleansing path?(Y, N): ").upper()

    if question.startswith("Y" or "Д"):

        print("\nAttention! Before deleting all files from the folder, some notes:")
        print("- For the correct removal of the insides of the folder, check if this folder is used for the operation of any program.")
        print("- All content is deleted permanently and there is no way to get it back!\n")

        while True:
            adding_to_list = input(
                "Name the final path to the folder, which will subsequently be completely cleaned up: ")

            if not os.path.isdir(fr"{adding_to_list}"):
                print("\nYou entered an invalid path or value. Please try again!")
            else:
                repositories.append(fr"{adding_to_list}")

            while True:
                True_break = None
                continue_or_again = input("\nDo you want to add more paths?(Y, N): ").upper()

                if continue_or_again.startswith("Y" or "Д"):
                    break

                if continue_or_again.startswith("N" or "Н"):
                    True_break = True
                    break

                else:
                    print("\nYou entered the wrong command, please try again!")

            if True_break:
                break
            else:
                pass

    else:
        pass

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

                for path, dirs, files in os.walk(repositories[0]):
                    for remove_dirs in dirs:
                        try:
                            os.rmdir(os.path.join(path, remove_dirs))
                            print(f"Removing... {remove_dirs}")
                        except (OSError, PermissionError):
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
