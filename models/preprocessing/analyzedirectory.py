import os

dr = 'C:\\Users\\Alisher\\Desktop\\Diplom_newVersion\\Tests\\'

def get_directories(directory):
    directories = []
    for path in os.listdir(directory):
        if os.path.isdir(dr + path):
            directories.append(dr + path)
    return directories

def get_files_in_directories(directory):
    files = []
    for path in os.listdir(directory):
        if path.find('.cpp'):
            files.append(directory +'\\'+ path)
    return files

def get_person_and_file(directory):
    directory = directory.split('\\')
    return directory[-2], directory[-1]

directories = get_directories(dr)
students = []
for path in directories:
    students.append(get_files_in_directories(path))

print(students)
print(get_person_and_file(students[0][0]))
