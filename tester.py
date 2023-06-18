#!/usr/bin/python3

import os
import sys
import subprocess
import colorama
import time
import platform

# Defines
COMPILE_COMMAND_WIN: str = "py AutoCompiler.py -c"
OUTPUT_PATH_WIN: str = "release/out"

COMPILE_COMMAND_LIN: str = "./AutoCompiler.py -c"
OUTPUT_PATH_LIN: str = "./release/out"

SPLASH_MSG = (
    colorama.Fore.CYAN
    + """
 █████╗  ██████╗██████╗ ██████╗     ███╗   ██╗ █████╗ ████████╗██╗██╗   ██╗███████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗    ████╗  ██║██╔══██╗╚══██╔══╝██║██║   ██║██╔════╝
███████║██║     ██████╔╝██████╔╝    ██╔██╗ ██║███████║   ██║   ██║██║   ██║█████╗  
██╔══██║██║     ██╔═══╝ ██╔═══╝     ██║╚██╗██║██╔══██║   ██║   ██║╚██╗ ██╔╝██╔══╝  
██║  ██║╚██████╗██║     ██║         ██║ ╚████║██║  ██║   ██║   ██║ ╚████╔╝ ███████╗
╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝         ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝
"""
)

# global Vars
system_os: str
Show_output = False
output_path: str

def main():
    colorama.init(autoreset=True)
    args = sys.argv

    global output_path
    global Show_output
    global system_os
    global TESTS_LIST
    
    print(SPLASH_MSG)
    
    # system adjustments
    system_os = platform.system()
    if system_os == "Windows":
        print("System adjustments for windows...")
        output_path = OUTPUT_PATH_WIN
        pass
    
    else:
        print("System adjustments for Linux...")
        output_path = OUTPUT_PATH_LIN
        pass

    if "-o" in args or "--ShowOutput" in args:
        Show_output = True
        pass

    if "-b" in args:
        #compiling
        if system_os == 'Windows':
            ret = os.system(COMPILE_COMMAND_WIN)
            pass

        else:
            ret = os.system(COMPILE_COMMAND_LIN)
            pass

        if ret == 0:
            #successed to compile
            print(
                colorama.Fore.GREEN
                + "The system has been build successsfuly"
                + colorama.Fore.RESET
            )
            print()
            pass

        else:
            # failed to compile
            sys.exit(
                colorama.Style.BRIGHT
                + colorama.Fore.RED
                + "Error Failed to build!"
                + colorama.Style.RESET_ALL
            )

        pass

    success_counter = 0
    print("=" * 7, " Tests ", "=" * 7)
    for test in TESTS_LIST:
        print("Running", test, "... ", end=colorama.Style.BRIGHT)
        
        #test start time
        start_time = time.time()
        
        #running test
        if TESTS_LIST[test]():
            success_counter += 1
            print(colorama.Fore.GREEN + "Successed! ", end="")
            pass

        else:
            print(colorama.Fore.RED + "Failed! ", end="")
            pass

        # printing how much time the test took
        print("[" + str(round(time.time() - start_time, 2)) + "'s]")
        print(end="")
        pass

    print()

    # results
    print(("=" * 9) + " Results: " + ("=" * 9))
    if success_counter == len(TESTS_LIST):
        temp = colorama.Fore.GREEN
        pass

    else:
        temp = colorama.Fore.RED
        pass

    temp = (
        temp
        + colorama.Style.BRIGHT
        + "["
        + str(success_counter)
        + " / "
        + str(len(TESTS_LIST))
        + "] "
        + "Tests Successed!"
    )
    print(temp)
    print(colorama.Style.RESET_ALL)


# tests methods
def test_help() -> bool:
    global output_path
    """
    testing if the help command work
    @return true if successed else return false if failed
    """
    ret = run_cmd([output_path, "--help"])
    return ret == 0


def run_cmd(cmd: list[str]):
    if Show_output:
        ret = os.system(" ".join(cmd))
        pass

    else:
        if system_os == "Windows":
            ret = subprocess.run(
                args=cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            ).returncode
            pass

        else:
            ret = subprocess.call(args=cmd,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.STDOUT)
        pass

    return ret


# tests list
TESTS_LIST = {"Help Test": test_help}

if __name__ == "__main__":
    main()
