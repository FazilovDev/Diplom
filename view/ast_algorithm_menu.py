from tkinter import *
from tkinter import filedialog as fd
import locale
from models.algorithms.AST import get_source_code_from_ast_detect, get_source_code_lines_from_file, get_str_from_list_code
from view.ast_git import get_points_clones
k = 15
q = 259#259
w = 4

class AstAlgorithmMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.pack(fill=BOTH, expand=True)
        self.file1 = 'file1'
        self.file2 = 'file2'
        self.top_frame = None

    def open(self):
        self.top_frame = Frame(self)
        self.top_frame.pack()
        self.top_frame.config(bg="white")

        self.twoFiles = Button(self.top_frame, text="Анализ 2х файлов", command=self.choice_count_twofiles)
        self.twoFiles.pack(side=LEFT)
        self.severalFiles = Button(self.top_frame, text="Анализ более двух файлов", command=self.choice_count_severalfiles)
        self.severalFiles.pack(side=LEFT)
        
    def close(self):
        self.destroy()
    
    def destroy_choice_button(self):
        self.twoFiles.destroy()
        self.severalFiles.destroy()

    def choice_count_twofiles(self):
        self.destroy_choice_button()
        self.show()
    
    def choice_count_severalfiles(self):
        self.destroy_choice_button()
        self.show_group_analyze()

    def choice_f1(self):
        self.file1 = fd.askopenfilename(defaultextension='.py', filetypes=[('Py', '.py')])
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1, self.file2)
        
    def choice_f2(self):
        self.file2 = fd.askopenfilename(defaultextension='.py', filetypes=[('Py', '.py')]) 
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1, self.file2)
    
    def print_file(self, code, points, side):
        if side == 0:
            textfield = self.text1
        else:
            textfield = self.text2

        textfield.delete(1.0,END)
        print(points)
        clear_start = 0
        for i in range(len(points)):
            start = points[i][0]
            end = points[i][1]

            if clear_start < start - 1:
                textfield.insert('end', get_str_from_list_code(code, clear_start, start-1))

            textfield.insert('end', get_str_from_list_code(code, start-1, end), 'warning')
            clear_start = end
        
        if clear_start < len(points)-1:
            textfield.insert('end', get_str_from_list_code(code, clear_start, len(points)))

        '''
        for i in range(len(text_code)):
            if i % 2 == 0:
                textfield.insert('end', text_code[i])
            else:
                textfield.insert('end', text_code[i], 'warning')
        '''

    def analyze(self):
        self.text1.tag_config('warning', background="orange",)
        self.text2.tag_config('warning', background="orange")

        points = get_points_clones([self.file1, self.file2])
        #self.text_plagiarism['text'] = "Уникальность файла: {} : {}%\nУникальность файла: {} : {}%".format(self.file1.split('/')[-1::][0], int(plag_percent), self.file2.split('/')[-1::][0], int(plag_percent2))
        self.print_file(get_source_code_lines_from_file(self.file1),points[self.file1], 0)
        self.print_file(get_source_code_lines_from_file(self.file2),points[self.file2], 1)

    def show(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        frame1.config(bg="white")
        self.text_info_menu = Label(frame1, text="Загрузите \n{} \n{}:".format(self.file1, self.file2), font=("Arial Bold", 20))
        self.text_info_menu.config(bg="white")
        self.text_info_menu.pack()

        self.text_plagiarism = Label(frame1, text="Уникальность файла: {} : {}%\nУникальность файла: {} : {}%".format("",0, "", 0), font=("Arial Bold", 20))
        self.text_plagiarism.config(bg="white")
        self.text_plagiarism.pack()
        choice_file2 = Button(frame1, text="Файл №2", command=self.choice_f2)
        choice_file2.pack(side=RIGHT, expand=True)
        choice_file1 = Button(frame1, text="Файл №1", command=self.choice_f1)
        choice_file1.pack(side=RIGHT, expand=True)
        
        frame2 = Frame(self)
        frame2.pack(fill=X)
        frame2.config(bg="white")
        analyze = Button(frame2, text="Обработать", command=self.analyze)
        analyze.pack()

        frame3 = Frame(self)
        frame3.pack(fill=X)
        frame3.config(bg="white")
        self.text1 = Text(frame3, width=int(100), height=int(100))
        self.text1.pack(side=LEFT)
        self.text2 = Text(frame3, width=int(100), height=int(100))
        self.text2.pack(side=LEFT)

    def choice_directory(self):
        self.directory = fd.askdirectory()
        self.text_directory['text'] = "Директория: {}".format(self.directory)
        self.button_choice_directory.destroy()

    def show_group_analyze(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        frame1.config(bg="white")

        self.button_choice_directory = Button(frame1, text="Выберите директорию с работами студентов", font=("Arial Bold", 11), command=self.choice_directory)
        self.button_choice_directory.pack()

        self.text_directory = Label(frame1, text="", font=("Arial Bold", 11))
        self.text_directory.config(bg="white")
        self.text_directory.pack()

        frame2 = Frame(self)
        frame2.pack(fill=X)
        frame2.config(bg="white")

