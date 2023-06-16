#!/usr/bin/python3
import hashlib
import json
import os
import platform
import sys
import time

from colorama import Fore, Style

# defines
CUSTOM_COMPILER_CAECH_FOLDER = ".AutoCompiler"
CODES_FILES_LIST_FILE = CUSTOM_COMPILER_CAECH_FOLDER + "/file_to_compile.dat"
COMPILE_HISTORY_LIST_FILE = CUSTOM_COMPILER_CAECH_FOLDER + "/compiled_files_History.dat"
COMPILE_CONFIG = CUSTOM_COMPILER_CAECH_FOLDER + "/compiled_links.dat"
COMPILE_CACHE = CUSTOM_COMPILER_CAECH_FOLDER + "/cache_objects"
FILES_TO_CHECK = CUSTOM_COMPILER_CAECH_FOLDER + "/FilesToCheck.dat"
INCLUDES_IN_FILES_LIST = CUSTOM_COMPILER_CAECH_FOLDER + "/includesInFiles.dat"

OBJECT_FILE_ENDING = ".obj"


OPTIMIZE_LEVEL_KEYWORD = "Optimize_level"
OUTPUT_FILE_KEYWORD = "Output_file"
SYSTEM_ADJUSTMENT_KEYWORD = "allow_System_adjustment"

# global varibales
Config: dict
system_os: str
 

# functions section:
def main():
    Starter()
    args = sys.argv[1:]

    if len(args) == 0:
        print("For Help please use the flag --help or -h")
        sys.exit("No args has been insert")

        # args = input("Option: ").split(" ")
        # pass

    if not os.path.exists(CODES_FILES_LIST_FILE):
        with open(CODES_FILES_LIST_FILE, "w") as f:
            f.close()

    if args[0] == "-n" or args[0] == "--add-new":
        if len(args) == 1:
            print("No Files paths")
            sys.exit(1)
            pass

        sys.exit(
            add_new_file(
                args[1:],
                (len(args) > 1 and (args[1] == "-a" or args[1] == "--auto-add-cpp")),
            )
        )
        pass

    elif args[0] == "-c" or args[0] == "--Compile":
        if len(args) > 1 and (args[1] == "-f" or args[1] == "--force"):
            sys.exit(gppCompileAllAtOnce())
        else:
            sys.exit(
                gppCompileSperate(
                    len(args) > 1
                    and (args[1] == "-r" or args[1] == "--rebuild-objects")
                )
            )
        pass

    elif args[0] == "-l" or args[0] == "--files-list":
        sys.exit(print_files_list((len(args) > 1 and args[1] == "-a")))

    elif args[0] == '-h' or args[0] == "--help":
        print_help()
        
    elif args[0] == "-f" or args[0] == "--flags":
        changeflags(args)

    else:
        print("unknown command")
        sys.exit(1)


def print_help():
    print(
        """Options:
-n / --add-new <file_path> = add new file to the file codes to compile
-c / --Compile = compiling all the files
-o / --Compile-optimized = Compile all the files with optimize
-s / --set-output-file <path>
-l / --files-list = get header files list
            
compile options:
-n / --no-linker = compile without using linker file compile all at once
-f / --force = force compiling all the files
-r / --rebuild-objects = rebuild all the objects
can't use force compile and no-linker at the same time the no-linker will get canceled

add-new options:
-a -auto-add-cpp = automaticly adding all the cpp files in the folders under the main one

files-list:
showing you list of all the files that been added to the list of the files to compile
"""
    )


def changeflags(args : list[str]):
    if len(args) == 1:
        print("No flags has been send")
        print("Current compile flag", Config[""])


# twice Slower than gppCompileSperate!!!
def gppCompileAllAtOnce():
    """
    just compiling all the files together into one file at once\n
    no object files or anything like that is used
    """
    print("compiling all at once")
    f = open(CODES_FILES_LIST_FILE, "r")
    Lines = f.readlines()
    cmd = "g++ -O" + Config[OPTIMIZE_LEVEL_KEYWORD] + " "

    for path in Lines:
        path = path[:-1]
        cmd += " " + path
    f.close()

    cmd += " -o " + Config[OUTPUT_FILE_KEYWORD]

    code_return = os.system(cmd)
    if code_return == 0:
        print(f"{Fore.GREEN}Compiled Successed! {Fore.RESET}")
    else:
        print(f"{Fore.RED}Failed To Compile (error: {code_return}){Fore.RESET}")
    return code_return


# TODO: MultiProcessing Compiling
# twice faster than gppCompileAllAtOnce!!
def gppCompileSperate(force: bool = False):
    """
    Compiling every file to sperate object file first and after that compiling all the object files together\n
    also after compiling a file into object it will save the file md5 in history file\n
    the idea of the history file is to not recompile file that has already compiled before\n
    returning the compiler return\n\n\n

    ------\n
    using the config file to know where to create the run file\n
    using the config file to know what is the optimize level to use
    """

    global Config
    has_File_Changed = dict()

    start_Time = time.time()
    print("Object compmiling!")
    print("loading file list...", end="")
    f = open(CODES_FILES_LIST_FILE, "r")
    code_files = list(map(lambda a: a[:-1], f.readlines()))
    f.close()
    print("Loaded")

    print("Loading History list ...", end=" ")
    f = open(COMPILE_HISTORY_LIST_FILE, "r")
    files_history = dict(json.load(f))
    f.close()
    print("Loaded")

    for code_path in code_files:
        if not (
            code_path in files_history
            and files_history[code_path] == md5_to_file(code_path)
        ):
            # print(code_path, "Changed checking for include changes") # DEBUG
            has_File_Changed[code_path] = True
            recognizeIncludes(code_path, False)
        else:
            has_File_Changed[code_path] = False

    # looking for files changes
    print("Looking for lib files chagnes!")
    with open(FILES_TO_CHECK, "r") as fp:
        while True:
            buffer = fp.readline()
            if buffer == "":
                break

            elif buffer[-1] == "\n":
                buffer = buffer[:-1]

            if (
                not force
                and buffer in files_history
                and files_history[buffer] == md5_to_file(buffer)
            ):
                has_File_Changed[buffer] = False
            else:
                has_File_Changed[buffer] = True
                files_history[buffer] = md5_to_file(buffer)

        fp.close()

    print("\n", "=" * 8, "included libs checked: ", "=" * 8)
    # print(has_File_Changed) # Debug
    for file_lib_Changed in has_File_Changed:
        if has_File_Changed[file_lib_Changed]:
            temp_string = Style.BRIGHT + Fore.YELLOW
        else:
            temp_string = Fore.CYAN

        print(
            temp_string,
            file_lib_Changed,
            "Has Changed: ",
            has_File_Changed[file_lib_Changed],
            Style.RESET_ALL,
        )

    print("=" * (len("included libs checked: ") + 16), "\n")

    # print(code_files) # Debug
    for code_path in code_files:
        file_name = code_path.split("/")[-1]
        object_file_path = (
            COMPILE_CACHE + "/" + file_name[: file_name.rfind(".")] + OBJECT_FILE_ENDING
        )
        # fix that it isn't checking if file that he included changed

        if (
            not force
            and not has_File_Changed[code_path]
            and os.path.exists(object_file_path)
            and is_included_lib_changed(code_path, has_File_Changed)
        ):
            print(f"object file of {code_path} already exists")

        else:
            if not has_File_Changed[code_path] or force:
                recognizeIncludes(code_path, False)

            print(f"Compiling object file for {code_path} ... ", end="")
            return_code = os.system("g++ -o " + object_file_path + " -c " + code_path)
            if return_code != 0:
                print(f"Error while compiling {code_path}")
                raise Exception(f"Error while compiling {code_path}")

            print(f"{Fore.GREEN}Compiled!{Fore.RESET}")
            files_history[code_path] = md5_to_file(code_path)

    print("===== All the object files compiled =====")
    f = open(COMPILE_HISTORY_LIST_FILE, "w")
    json.dump(files_history, f)
    f.close()

    # create a check to all the files that he include
    # the algoritm:
    # get list of all the include files that he got
    # after that we will add them to the history list but not to compile list
    # we will check if they have changed with the new check by the next idea we will
    # we will check all the files that have connection with that file
    # we will create a check to all file another function that will save all the
    # cpp files that connected with that file
    # so if we will recompile and the file isn't matching has last time we will need to recompile

    objects_list = list(
        map(lambda a: COMPILE_CACHE + "/" + a, os.listdir(COMPILE_CACHE))
    )

    # adding .exe if the operation system is windows
    exe_output = str(Config[OUTPUT_FILE_KEYWORD])
    if (
        system_os == "Windows"
        and str(Config[SYSTEM_ADJUSTMENT_KEYWORD]).lower() == "true"
    ):
        if exe_output[exe_output.rfind(".") :] != ".exe":
            exe_output += ".exe"
            print("Output file path changed for System Adjustments")

    print(
        "\nStarting final Build...\nOutput file: "
        + exe_output
        + "\nOptimize level: "
        + Config[OPTIMIZE_LEVEL_KEYWORD]
        + "\nSystem adjustments: "
        + str(str(Config[SYSTEM_ADJUSTMENT_KEYWORD]).lower() == "true")
        + "\n"
    )

    print("Compiling...")

    return_code = os.system(
        "g++ -o "
        + exe_output
        + " -O"
        + Config[OPTIMIZE_LEVEL_KEYWORD]
        + " "
        + " ".join(objects_list)
    )
    if return_code == 0:
        print(
            f"{Style.BRIGHT}{Fore.GREEN}====== Compiled Successfuly {round(time.time() - start_Time, 2)}'s ======"
            + f"{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Style.BRIGHT}{Fore.RED}====== Failed To Compile!!! ======"
            + f"{Style.RESET_ALL}"
        )

    return return_code


def remove_old_libs_from_checklist() -> None:
    """
    Checking that the Files check dat file is
        all the info in it still valid
    """
    with open(FILES_TO_CHECK, "r") as fp:
        files_lst: list[str] = []
        while True:
            buffer = fp.readline()
            if buffer == "":
                break
            elif buffer[-1] == "\n":
                buffer = buffer[:-1]
            files_lst += [buffer]

        fp.close()
        pass

    # checking if the file exists
    print("Checking if all files still exists")

    for lib in files_lst:
        if not os.path.exists(lib):
            print(f"removing {lib} non existing (anymore) file from list")
            files_lst.remove(lib)

    with open(FILES_TO_CHECK, "w") as fp:
        for lib in files_lst:
            fp.write(str(lib + "\n"))
        fp.close()
        pass
    pass


def is_included_lib_changed(path: str, changed_files: dict) -> bool:
    with open(INCLUDES_IN_FILES_LIST, "r") as f:
        current_includes = dict(json.load(f))
        f.close()

    if ("./" + path) in current_includes:
        path = "./" + path

    elif path.find("./") == 0 and path[len("./") :] in current_includes:
        path = path[len("./") :]

    includes_of_path = current_includes[path]
    for lib in includes_of_path:
        if changed_files[lib]:
            print(lib, changed_files[lib])
            return False

    return True


def recognizeIncludes(path: str, deep_check: bool = False):
    ALLOWED_SYMBOLS = ["#", "/", "\n"]
    current_directory = "./"

    file_paths: list[str] = [path]
    # getting the includes that already has been added
    with open(INCLUDES_IN_FILES_LIST, "r") as f:
        current_includes = dict(json.load(f))
        f.close()
    print("Include file list Loaded")

    with open(FILES_TO_CHECK, "r") as f:
        list_of_check_files = set()
        buffer = "Buffer isn't empty"
        while buffer != "":
            buffer = f.readline()
            # print(buffer) # debuging
            if buffer == "":
                break

            if buffer[-1] == "\n":
                buffer = buffer[:-1]

            list_of_check_files.add(buffer)

        f.close()

    print("Files check list loaded")
    # print(list(list_of_check_files)) # debuging

    print("Getting file includes of " + path)

    for file_path in file_paths:
        # print("Reading file " + file_path) #debuging
        fp = open(file_path, "r")
        buffer = "file read buffer"

        while not buffer == "":
            buffer = removing_starting_spaces(str(fp.readline()))
            # print(buffer) # debugging

            # checking if the buffer is legal
            if buffer == "":
                break

            elif buffer[0] not in ALLOWED_SYMBOLS and not deep_check:
                break

            elif "#include" not in buffer:
                continue

            if buffer[: len("#include")] == "#include":
                # checking if that library is legal
                if "<" in buffer or ">" in buffer:
                    continue

                lib_name = buffer[buffer.find('"') + 1 : buffer.rfind('"')]

                if not os.path.exists(lib_name):
                    if os.path.exists(file_path[: file_path.rfind("/") + 1] + lib_name):
                        lib_name = file_path[: file_path.rfind("/") + 1] + lib_name

                lib_name = path_Shorter(lib_name)

                if lib_name not in file_paths:
                    # create path shorter
                    list_of_check_files.add(lib_name)
                    file_paths += [lib_name]

        fp.close()

    file_paths.remove(path)

    # writing to file the list of file that will change the path file we checked
    current_includes[path] = file_paths
    with open(INCLUDES_IN_FILES_LIST, "w") as f:
        json.dump(current_includes, f)
        print("Written to file list to include")
        f.close()

    # writing to file the list of files we will need to checkat compilation
    with open(FILES_TO_CHECK, "w") as f:
        f.writelines(list(map(lambda a: a + "\n", list(list_of_check_files))))
        print("writen to file list to check")
        f.close()

    # we will create to list
    # one of file to check if changed
    # and the other list will include all the includes of files
    # including the parent libraries that has been included

    # we need to save it in a file after we check using

    # json could be the smartest way


def path_Shorter(path: str) -> str:
    # remove ..
    while "/../" in path:
        if path.find("/../") == -1:
            break

        if path[: path.find("/../")].rfind("/") == -1:
            path = path[path.find("/../") + len("/../") :]

        else:
            path = (
                path[: path[: path.find("/../")].rfind("/")]
                + path[path.find("/../") + len("/../") - 1 :]
            )

    while "/./" in path:
        if path.find("/./") == -1:
            break

        if path[: path.find("/./")].rfind("/") == -1:
            path = path[path.find("/./") + len("/./") :]

        else:
            path = (
                path[: path[: path.find("/./")].rfind("/")]
                + path[path.find("/./") + len("/./") - 1 :]
            )

    if path[:2] == "./":
        path = path[2:]

    return path


def removing_starting_spaces(sentance: str):
    count = 0
    for i in sentance:
        if i != " ":
            break
        count += 1

    return sentance[count:]


def add_new_file(File_to_load: list[str], auto_add_all_cpp: bool = False):
    """
    == Adding to the file "list to compile" the list of file
    that sended to compile ==\n
    if the auto_add_all_cpp is true complatly ignore the\n
    files_to_load list sended and instead auto adding all the files\n
    under the parent folder that have the ending .cpp\n
    *ignoring all the files that isn't ending with .cpp\n\n

    returning 0 if all the files has been added successfuly
    """

    fp = open(CODES_FILES_LIST_FILE, "r")
    code_files = list(map(lambda a: a.replace("\n", ""), fp.readlines()))
    fp.close()

    if auto_add_all_cpp:
        File_to_load = ["."]
        for path in File_to_load:
            if os.path.isdir(path) and path.rfind(".") == 0:
                File_to_load += list(map(lambda a: path + "/" + a, os.listdir(path)))

            elif os.path.isdir(path) and path.rfind(".") != 0:
                File_to_load.remove(path)

    File_to_load = list(
        filter(lambda a: ".cpp" in a and a not in code_files, File_to_load)
    )

    shorted_file_list = []
    for file_path in File_to_load:
        shorted_file_list += [path_Shorter(file_path)]

    File_to_load = []
    for shoted_file in shorted_file_list:
        if shoted_file not in code_files:
            File_to_load += [shoted_file]

    f = open(CODES_FILES_LIST_FILE, "a")
    if File_to_load == []:
        print("no files has been added")
        pass

    else:
        print("Added File to compile: \n", "\n+".join(File_to_load))
        pass

    for path in File_to_load:
        f.write(path + "\n")
        recognizeIncludes(path, False)
        print(f"{path} added")

    f.close()
    return 0


def print_files_list(print_all_files: bool):
    """
    printing all the .cpp files that are in the list
    if print print_every_file true printing everything
    """
    if print_all_files:
        print("Printing all the files in the list")

    f = open(CODES_FILES_LIST_FILE, "r")
    Lines = f.readlines()
    # print(Lines) # debug
    f.close()

    check_libs = []
    with open(FILES_TO_CHECK, "r") as fp:
        while True:
            buffer = fp.readline()
            if buffer == "":
                break

            if buffer[-1] == "\n":
                buffer = buffer[:-1]

            check_libs += [buffer]

        fp.close()

    print(Style.BRIGHT + "Files list to compile: ")
    Lines = list(map(lambda a: a[:-1], Lines))

    for path in Lines:
        if path[path.rfind(".") :] == ".cpp" or path[path.rfind(".") :] == ".h":
            if (
                path[: path.rfind(".")] + ".h" in check_libs
                or path[: path.rfind(".")] + ".hpp" in check_libs
            ):
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}{path[:path.rfind('.')] + '.hpp'} -- header file for {path} found{Fore.RESET}"
                )

            else:
                print(
                    f"{Fore.CYAN}{path[:path.rfind('.')] + '.hpp'} -- header file for {path} hasn't found{Fore.RESET}"
                )

        elif print_all_files:
            print(f"{Fore.CYAN}{path}")

    return 0


def md5_to_file(path: str) -> str:
    """
    Doing md5 Hash to the file sended in args
    """
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def Starter():
    """
    checking if all the files that should be exists exist
    if not creating include dirs
    """
    global Config
    global system_os

    print("Starting...")

    # checking the platform system
    system_os = platform.system()
    if system_os == "Windows" or system_os == "Linux":
        print("[Note]The System running on", system_os)
        pass

    else:
        print("Warning: The system used is", system_os)
        print("Warning: the system isn't in the list and could have some problem\n")

    if os.system("g++ --version") != 0:
        print("Error g++ hasn't found")
        sys.exit(7)

    # checking if the main folder exists
    if not os.path.exists(CUSTOM_COMPILER_CAECH_FOLDER):
        os.mkdir(CUSTOM_COMPILER_CAECH_FOLDER)
        print("Settings folder created")

    # checking if the main folder is folder
    elif not os.path.isdir(CUSTOM_COMPILER_CAECH_FOLDER):
        print(f"We need to override the {CUSTOM_COMPILER_CAECH_FOLDER} file")
        choice = input("Do U allow to override the file: ")
        if choice.lower() == "y":
            os.remove(CUSTOM_COMPILER_CAECH_FOLDER)
        else:
            print("Unfortuntly the system can't work without that file")
            sys.exit(1)

    if not os.path.exists(COMPILE_CACHE):
        os.mkdir(COMPILE_CACHE)
        print("Cache objects folder created")

    # checking if the main folder is folder
    elif not os.path.isdir(COMPILE_CACHE):
        print(f"We need to override the {COMPILE_CACHE} file")
        choice = input("Do U allow to override the file: ")
        if choice.lower() == "y":
            os.remove(COMPILE_CACHE)
        else:
            print("Unfortuntly the system can't work without that file")
            sys.exit(1)

    if not os.path.exists(COMPILE_CONFIG):
        CreateConfigFile("", True)
        print("ConfigFile Has been created")

    if not os.path.exists(INCLUDES_IN_FILES_LIST):
        fp = open(INCLUDES_IN_FILES_LIST, "w")
        fp.write("{}")
        fp.close()

        print("Includes list file created!")

    if not os.path.exists(FILES_TO_CHECK):
        fp = open(FILES_TO_CHECK, "w")
        fp.close()

        print("file check list file created!")

    fp = open(COMPILE_CONFIG, "r")
    Config = dict(json.load(fp))
    fp.close()
    print("config loaded")

    if not os.path.exists(COMPILE_HISTORY_LIST_FILE):
        fp = open(COMPILE_HISTORY_LIST_FILE, "w")
        fp.write("{}")
        fp.close()
        print("History File Created")

    if not os.path.exists(CODES_FILES_LIST_FILE):
        fp = open(CODES_FILES_LIST_FILE, "w")
        fp.write("")
        fp.close()
        print("Codes list file created")

    remove_old_libs_from_checklist()
    print("============\n")
    return


# TODO
def CreateConfigFile(args, default=False):
    """
    Just creating simple config file nothing more right now
    """

    args = args.split(" ")
    fp = open(COMPILE_CONFIG, "w")

    temp = None

    # write the json
    output_file = "release/out"
    optimize_level = 3
    system_adjustment = "True"

    arg_dict = {"-o": output_file, "-O": optimize_level, "-s": system_adjustment}

    for arg in args:
        if arg in arg_dict:
            print("Found in args")
            print(arg_dict[arg])

    fp.write(
        "{"
        + f'"{OUTPUT_FILE_KEYWORD}":"{output_file}",'
        + f' "{OPTIMIZE_LEVEL_KEYWORD}": "{optimize_level}",'
        + f' "{SYSTEM_ADJUSTMENT_KEYWORD}": "{system_adjustment}"'
        + "}"
    )

    fp.close()
    pass


if __name__ == "__main__":
    main()
