"""
Author: Oliver Gaither
Date: 2/2/2022
Description: generate C++, headers, python, python packages and more
"""
import libog
import sys
import os
from datetime import datetime
import time

def writefile(fname, lines):
    """
    create file
    :param fname:
    :param lines:
    :return:
    """
    with open(fname, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def readfile(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def get_valid_str(q, params):
    """
    validate a string based on given acceptable
    responses
    :param q:
    :param params:
    :return:
    """
    r = input(q)
    while r not in params:
        r = input("invalid\n" + q)
    return r


def get_todays_date():
    """ return string formatted version of the current date and time"""
    n = datetime.now()
    return n.strftime("%m/%d/%Y %H:%M:%S")


def getinfo(dontprompt):
    data_path = os.path.join(os.getcwd(), '.fleauxData')
    if (dontprompt):
        r = readfile(data_path)
        author, email = r
    else:
        author = input("your name: ")
        email = input("your email: ")
        writefile(data_path, f"{author}\n{email}")
    return author, email



def headercomment(fname, ftype, proj_name, author, email):
    """ returns header comment formatted for UMBC CMSC202 standards """
    return f"""/*********************************************
* File:    {fname}.{ftype}
* Project: {proj_name}
* Author:  {author}
* Date:    {get_todays_date()}
* Email:   {email}
* Purpose:
**********************************************/
"""


def choose_directory():
    """
    lets user choose which directory to create files in
    or create the directory all together
    """
    r = input("which directory shall the files reside? (can be brand new!):  ")
    path = os.path.join(os.path.abspath(os.getcwd()), r)
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

    

    
def classdef(fname):
    return f"class {fname.title()}\n" \
           f"{'{'}\n" \
           f"\tpublic:\n" \
           f"\tprivate:\n" \
           f"{'}'};"


def headerguards(fname):
    return f"#ifndef {fname.upper()}_H\n" \
           f"#define {fname.upper()}_H\n\n" \
           f"{classdef(fname)}\n" \
           f"#endif"


def create_entry():
    return "#include <iostream>\n\n" \
           "int main(int argc, char *argv[])\n" \
           "{\n" \
           "\treturn 0;\n" \
           "}\n"


def display_finish_message(t):
    """
    message to display destination directory and files
    along with total file creation time and the end of
    the program
    :param t:
    :return:
    """
    sys.stdout.write("\n")
    s = "process finished in: " +  libog.bold("{:.4f}ms".format(t*1000))
    print(libog.add_color(s, color="purple"))
    print(f"Directory - {libog.add_color(libog.underline(os.getcwd()), color='green')}")
    os.system("ls -l")
    print(libog.bold("Get out there and code!\n"))
    
    
def create_makefile(fname, headers=None):
    """
    creates Makefile to go along with new 
    C++ code files
    """
    if headers:
        headers = []
    return f"{fname}: {fname}.cpp\n"\
            f"\tg++ -Wall {fname}.cpp -o {fname}"


def make_class_files(fname):
    """
    make a header and its respective cpp
    file
    """
    data_path = os.path.join(os.getcwd(), ".fleauxData")
    exists = False
    if (os.path.exists(data_path)):
        exists = True
    author, email = getinfo(exists)
    choose_directory()
    fname = fname.title()
    assignment = input("assignment name: ")
    start = time.perf_counter()
    hfile = headercomment(fname, 'h', assignment, author, email) + headerguards(fname)
    cppfile = headercomment(fname, 'cpp', assignment, author, email) + f'#include "{fname}.h"\n'+ classdef(fname)
    writefile(fname + '.h', hfile)
    writefile(fname + '.cpp', cppfile)
    stop = time.perf_counter()
    display_finish_message(stop-start)


def make_regular(fname):
    """
    make a single cpp file, typically
    an entry point for a program
    :param fname:
    :return:
    """
    data_path = os.path.join(os.getcwd(), ".fleauxData")
    exists = False
    if (os.path.exists(data_path)):
        exists = True
    author, email = getinfo(exists)
    choose_directory()
    assignment = input("assignment name: ")
    start = time.perf_counter()
    file = headercomment(fname, 'cpp', assignment, author, email) + create_entry()
    writefile(fname + '.cpp', file)
    writefile("Makefile", create_makefile(fname))
    stop = time.perf_counter()
    display_finish_message(stop-start)


def generate_python_bp(fname, author, email):
    return f'"""\n' \
            f'File: {fname}\n'\
            f'Author: {author}\n'\
            f'Date: {get_todays_date()}\n'\
            f'Email: {email}\n' \
            f'Description:\n'\
            f'"""\n\n\n'\
            f'if __name__ == "__main__":\n'\
            f'\tpass\n'


def make_python(fname):
    """
    generates and writes a python file
    """
    data_path = os.path.join(os.getcwd(), ".fleauxData")
    exists = False
    if (os.path.exists(data_path)):
        exists = True
    author, email = getinfo(exists)
    choose_directory()
    start = time.perf_counter()
    fname = fname + '.py'
    pyfile = generate_python_bp(fname, author, email)
    writefile(fname, pyfile)
    stop = time.perf_counter()
    display_finish_message(stop-start)


def setup_with_console():
    """
    serves as an option for the case that this program
    is run without any arguments on the command line, along
    with debugging in an IDE console run environment
    :return:
    """
    fname = input("filename: ")
    ftype = get_valid_str("filetype (h, cpp, py): ", ['h',"cpp", "py"])
    if ftype == 'h':
        make_class_files(fname)
    elif ftype == 'cpp':
        make_regular(fname)
    elif ftype == 'py':
        make_python(fname)
    
def documentation():
    print(libog.decorate("How to Fleaux", undline=True, makebold=True))
    print("fleaux [filename] [filetype (h, cpp, py)]")
    print("or")
    print("fleaux --update (to update fleauxData)")

def main():
    if len(sys.argv) > 3 or len(sys.argv) == 1:
        documentation()
        sys.exit(-1)
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == "--update":
                getinfo(dontprompt=False)
                print(libog.bold(libog.add_color("Name and email updated succesfully.", "green")))
            elif sys.argv[1] == "-h":
                documentation()
            else:
                documentation()
        else:
            if sys.argv[2] not in ['h','cpp', 'py']:
                documentation()
                sys.exit(-1)
            if sys.argv[2] == 'h':
                make_class_files(sys.argv[1])
            elif sys.argv[2] == "cpp":
                make_regular(sys.argv[1])
            elif sys.argv[2] == "py":
                make_python(sys.argv[1])


if __name__ == '__main__':
    main()