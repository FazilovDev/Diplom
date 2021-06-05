import os

#dr = '\\Tests\\set\\'

def get_directories(directory):
    directories = []
    for path in os.listdir(directory):
        if os.path.isdir(directory + path):
            directories.append(directory + path)
    return directories

def get_files_in_directories(directory, extended):
    files = []
    for path in os.listdir(directory):
        if path.endswith(extended) :
            files.append(directory +'\\'+ path)
    return files

def get_person_and_file(directory):
    directory = directory.split('\\')
    return directory[-2], directory[-1]

#print(get_files_in_directories(dr,'.cpp'))
'''
directories = get_directories(dr)
students = []
for path in directories:
    students.append(get_files_in_directories(path))

print(students)
print(get_person_and_file(students[0][0]))
'''