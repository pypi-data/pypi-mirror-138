import os, sys, pickle, json
from collections import namedtuple

# = Clear

def clear():  
    """Clears terminal"""
    os.system("cls" if os.name == "nt" else "clear")

# = pickle lister

def depickler(filename):
    """writes object to list from file"""
    with open(os.path.join(sys.path[0], f"{filename}.pickle"), "rb") as pickle_file:
        objects = []
        while True:
            try:
                objects.append(pickle.load(pickle_file))
            except EOFError:
                break
    return objects

# = file to list converter

def file_lister(file):
    """takes file as string input, a variable for the file (it can be whatever as long as it is changeable) and an empty list as input"""
    with open(os.path.join(sys.path[0], file), "r") as file_variable:
        file_list = file_variable.readlines()  # ¤ writes file content to list
        for i in range(len(file_list)):  # ¤ strips the content of the list
            file_list[i] = file_list[i].strip()
    return file_list  # ¤ returns the list

# = integer input checker

def intput(printable, value_error_text = "You didnt write a number."):
    """Makes an int from input by trying the input until it doesnt crash"""
    while True:
        try:
            return int(input(printable))

        except ValueError:
            clear()
            print(value_error_text)

# = pickle saver

def picklify(obj_list, filename):
    """Saves object to file"""
    with open(os.path.join(sys.path[0], f"{filename}.pickle"), "wb") as file:  # ¤ Overwrites any existing file.
        for i in range(len(obj_list)):
            pickle.dump(obj_list[i], file, pickle.HIGHEST_PROTOCOL)
        file.close()

# = string integer input checker

def strintput(printable, value_error_text = "You didnt write a number."):
    """Makes a string from an integer taken from input by trying input until it doesnt crash"""
    while True:
        try:
            stringput = input(printable)
            return (
                "0" + str(int(stringput))
                if stringput.startswith("0")
                else str(int(stringput))
            )


        except ValueError:
            clear()
            print(value_error_text)

# = read from json file

def json_reader(filename):
    """reads from json file and returns dict"""
    with open(os.path.join(sys.path[0], f'{filename}.json'), "r") as read_file:
        return json.load(read_file)


# = write to json file

def json_writer(data, filename):
    """writes dict to json"""
    with open(os.path.join(sys.path[0], f'{filename}.json'), "w") as write_file:
        json.dump(data.__dict__.items(), write_file)
