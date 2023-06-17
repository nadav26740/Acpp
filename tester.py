import os
import sys
import subprocess
import colorama
import time

# Defines
COMPILE_COMMAND: str = "py AutoCompiler.py -c"
OUTPUT_PATH: str = "release\\out.exe"
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
Show_output = False


def main():
    colorama.init(autoreset=True)
    args = sys.argv
    global Show_output
    global TESTS_LIST
    print(SPLASH_MSG)

    if "-o" in args or "--ShowOutput" in args:
        Show_output = True
        pass

    if "-b" in args:
        #compiling
        ret = os.system(COMPILE_COMMAND)
        
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
    """
    testing if the help command work
    @return true if successed else return false if failed
    """
    ret = run_cmd([OUTPUT_PATH, "--help"])
    return ret == 0


def run_cmd(cmd: list[str]):
    if Show_output:
        ret = os.system(" ".join(cmd))
        pass

    else:
        ret = subprocess.run(
            args=cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        ).returncode
        pass

    return ret


# tests list
TESTS_LIST = {"Help Test": test_help}

if __name__ == "__main__":
    main()
