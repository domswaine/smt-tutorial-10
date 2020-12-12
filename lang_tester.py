from subprocess import run, PIPE
from os import path
import sys

def file_exists(filepath: str) -> bool:
    return path.isfile(filepath)

arguments = sys.argv
files_to_test = set()
for argument in arguments:
    if not argument.endswith("lang_tester.py") and file_exists(argument):
        files_to_test.add(argument)
del arguments

for file_to_test in files_to_test:
    status_target, stdout_target = None, None

    with open(file_to_test, "r") as infile:
        headerLines = infile.readlines()[:2]

        for line in headerLines:
            if line[0] == "#":
                p_line = line[1:].strip()
                if p_line.startswith("status:"):
                    status_target = p_line.lstrip("status:").lstrip()
                elif p_line.startswith("stdout:"):
                    stdout_target = p_line.lstrip("stdout:").lstrip()
                del p_line

    program_run = run(["python3", file_to_test], stdout=PIPE)
    status = "success" if program_run.returncode == 0 else 'failure'
    stdout = program_run.stdout.decode().partition('\n')[0]
    del program_run

    if status == status_target and stdout == stdout_target:
        print("{filename}: success".format(filename = file_to_test))
    else:
        print("{filename}: failure".format(filename = file_to_test))