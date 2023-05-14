# Program to check whether a library is present in Cocoapods dependency manager
# Program requires a file with names of the libraries present in it


import os

cocoapods = []
non_cocoa = []

file_path = input("Path (Absolute is preferred) of the input file: ")
with open(file_path) as f:                                  # file with the name of the libraries
    libraries = [line.rstrip() for line in f]

for lib in libraries:
    flag = 0
    os.system("pod search {} >> tmp".format(lib))       # intermediate file "tmp"

    with open('tmp') as f:
        no_of_lines = len(f.readlines())            # check for if the file is empty
    
    if (no_of_lines == 0):
        print("Library is not present in Cocoapods")        # "tmp" file is empty
        flag = 1
        non_cocoa.append(lib)
        continue
    elif (no_of_lines > 1):
        check = os.system('cat tmp | grep -G " {} " >> grep_op'.format(lib))
        os.remove('grep_op')
        if not (check):         # Keyword exists hence pod exist in cocoapods
            cocoapods.append(lib)             # check = 0 ==> grep returned with error code 0
            check = os.system('cat tmp | head | grep -G "Versions:" >> ver_op')
            with open('ver_op') as file:
                ver_line = file.readline()
                print("--- " + lib)
                x = ver_line.index("Versions:") + len("Versions: ")
                versions = ver_line[x::].replace(",", "").split(" ")[:-2]        # last two elements are '[trunk' & 'repo]'
                print(versions)
            os.remove('ver_op')
        else:
            non_cocoa.append(lib)
        os.remove('tmp')

print("-> Non Cocoapods: ")
print(non_cocoa)
