from tkinter import *
from tkinter import filedialog as fd
import locale
from tkinter import messagebox
from models.algorithms.winnowing import get_fingerprints, get_text_from_file
from models.preprocessing.analyzedirectory import get_files_in_directories
#k = 21#17#17 #15
q = 259#259
#w = 8 #4

LANGUAGES = ['PYTHON', 'C++', 'JAVA', 'SWIFT']
FILES = {'PYTHON' : '.py', 'C++' : '.cpp', 'JAVA' : '.java', 'SWIFT' : '.swift'}

#Оптимальные значения k = 8 w = 3
class MossAlgorithmMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.pack(fill=BOTH, expand=True)
        self.file1 = 'file1'
        self.file2 = 'file2'
        self.directory = ''
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
        self.file1 = fd.askopenfilename(defaultextension='.py', filetypes=[('Py', '.py'), ('CPP', '.cpp'),('TXT', '.txt'),('SWIFT','.swift'),('JAVA','.java')])
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1.split('/')[-1], self.file2.split('/')[-1])
        
    def choice_f2(self):
        self.file2 = fd.askopenfilename(defaultextension='.py', filetypes=[('Py', '.py'), ('CPP', '.cpp'),('TXT', '.txt'),('SWIFT','.swift'),('JAVA','.java')])   
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1.split('/')[-1], self.file2.split('/')[-1])
    
    def print_file1(self,text, points, side):
        newCode = text[: points[0][0]]
        if side == 0:
            textfield = self.text1
        else:
            textfield = self.text2
        textfield.delete(1.0,END)
        textfield.insert('end', newCode)
        plagCount = 0
        for i in range(len(points)):
            if points[i][1] > points[i][0]:
                plagCount += points[i][1] - points[i][0]
                newCode = newCode  + text[points[i][0] : points[i][1]]
                textfield.insert('end', text[points[i][0] : points[i][1]], 'warning')
                if i < len(points) - 1:
                    newCode = newCode + text[points[i][1] : points[i+1][0]]
                    textfield.insert('end', text[points[i][1] : points[i+1][0]])
                else:
                    newCode = newCode + text[points[i][1] :]
                    textfield.insert('end', text[points[i][1] :])
        return plagCount / len(text)

    def analyze(self):
        self.text1.tag_config('warning', background="orange",)
        self.text2.tag_config('warning', background="orange")
        text1 = get_text_from_file(self.file1)
        text2 = get_text_from_file(self.file2)

        try:
            mergedPoints = get_fingerprints(self.file1, self.file2, self.k.get(), self.q.get(), self.w.get())
            res = self.print_file1(text1, mergedPoints[0], 0)
            res1 = self.print_file1(text2, mergedPoints[1], 1)
            self.text_similarity['text'] = "Расстояние Жаккара: {0:4.4f}".format(mergedPoints[2])
            self.text_plagiarism['text'] = "Уникальность файла: {} : {}%\nУникальность файла: {} : {}%".format(self.file1.split('/')[-1::][0], int((1-res)*100), self.file2.split('/')[-1::][0], int((1-res1)*100))
        except Exception as e:
            messagebox.showinfo("Ошибка!", str(e))

    def show(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        frame1.config(bg="white")
        self.text_info_menu = Label(frame1, text="Загрузите \n{} \n{}:".format(self.file1, self.file2), font=("Arial Bold", 18))
        self.text_info_menu.config(bg="white")
        self.text_info_menu.pack()

        self.text_plagiarism = Label(frame1, text="Уникальность файла: {} : {}%\nУникальность файла: {} : {}%".format("",0, "", 0), font=("Arial Bold", 14))
        self.text_plagiarism.config(bg="white")
        self.text_plagiarism.pack()
        self.text_similarity = Label(frame1, text="Расстояние Жаккара: 0", font=("Arial Bold", 20))
        self.text_similarity.config(bg="white")
        self.text_similarity.pack()

        choice_file2 = Button(frame1, text="Файл №2", command=self.choice_f2)
        choice_file2.pack(side=RIGHT, expand=True)
        choice_file1 = Button(frame1, text="Файл №1", command=self.choice_f1)
        choice_file1.pack(side=RIGHT, expand=True)

        frame4 = Frame(self)
        frame4.pack(fill=X)
        frame4.config(bg="white")

        self.text_k = Label(frame4, text="Размер граммы k:")
        self.text_k.config(bg="white")
        self.text_k.pack()
        self.k = IntVar()
        self.k_entry = Entry(frame4,textvariable=self.k)
        self.k_entry.pack()
        self.k.set(8)


        self.text_w = Label(frame4, text="Размер окна w:")
        self.text_w.config(bg="white")
        self.text_w.pack()
        self.w = IntVar()
        self.w_entry = Entry(frame4,textvariable=self.w)
        self.w_entry.pack()
        self.w.set(3)

        self.text_q = Label(frame4, text="Величина Q:")
        self.text_q.config(bg="white")
        self.text_q.pack()
        self.q = IntVar()
        self.q_entry = Entry(frame4,textvariable=self.q)
        self.q_entry.pack()
        self.q.set(701)
        
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
        #self.button_choice_directory.destroy()
    

    def show_result(self, results):
        self.result_analyzer.delete(1.0,END)
        for res in results:
            if res[2] > 0.5 and res[2] < 0.75:
                self.result_analyzer.insert('end', str(res[0].split('/')[-1::][0]) + ' -> ' + str(res[1].split('/')[-1::][0]) + ' : ' + '{0:4.4f}'.format(100*res[2]) +'%\n', 'warning')
            elif res[2] >= 0.75:
                self.result_analyzer.insert('end', str(res[0].split('/')[-1::][0]) + ' -> ' + str(res[1].split('/')[-1::][0]) + ' : ' + '{0:4.4f}'.format(100*res[2]) +'%\n', 'plag')
            else:
                self.result_analyzer.insert('end', str(res[0].split('/')[-1::][0]) + ' -> ' + str(res[1].split('/')[-1::][0]) + ' : ' + '{0:4.4f}'.format(100*res[2]) +'%\n')

    def analyzer_several_files(self, language):
        files = get_files_in_directories(self.directory, FILES[language])
        if len(files) < 2:
            messagebox.showerror('Ошибка', 'Не найдены файлы на заданном языке')
            return
        results = []
        if self.full_info.get() == 0:
            for i in range(len(files)):
                for j in range(len(files)):
                    if i != j:
                        res = get_fingerprints(files[i], files[j], self.k.get(), self.q.get(), self.w.get())
                        if res != None:
                            results.append([files[i], files[j], res[2]])
        else:
            for i in range(len(files)):
                max_plag = 0
                max_file = ''
                for j in range(len(files)):
                    if i != j:
                        res = get_fingerprints(files[i], files[j], self.k.get(), self.q.get(), self.w.get())
                        if res != None and res[2] > max_plag:
                            max_plag = res[2]
                            max_file = files[j]
                results.append([files[i], max_file, max_plag])
        
        self.show_result(results)
    
    def get_plag(self):
        selection = self.languages.curselection()
        if (selection == None or len(selection) == 0):
            messagebox.showerror("Ошибка", 'Вы не выбрали язык')
            return
        if (self.directory == None or self.directory == ''):
            messagebox.showerror("Ошибка", 'Вы не выбрали директорию')
            return
        language = self.languages.get(selection[0])
        
        self.analyzer_several_files(language)

    def show_group_analyze(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        frame1.config(bg="white")

        self.button_choice_directory = Button(frame1, text="Выберите директорию с работами студентов", font=("Arial Bold", 11), command=self.choice_directory)
        self.button_choice_directory.pack()

        self.text_directory = Label(frame1, text="", font=("Arial Bold", 11))
        self.text_directory.config(bg="white")
        self.text_directory.pack()

        self.full_info = BooleanVar()
        self.full_info.set(0)
        r1 = Radiobutton(frame1, text='полная информация', variable=self.full_info, value=0)
        r1.pack()

        r2 = Radiobutton(frame1, text='краткая инфорация', variable=self.full_info, value=1)
        r2.pack()
        
        frameTools = Frame(self)
        frameTools.pack(side=LEFT)
        frameTools.config(bg="white")

        frameParams = Frame(frameTools)
        frameParams.pack()
        frameParams.config(bg="white")

        self.text_k = Label(frameParams, text="Размер граммы k:")
        self.text_k.config(bg="white")
        self.text_k.pack()
        self.k = IntVar()
        self.k_entry = Entry(frameParams,textvariable=self.k)
        self.k_entry.pack()
        self.k.set(8)


        self.text_w = Label(frameParams, text="Размер окна w:")
        self.text_w.config(bg="white")
        self.text_w.pack()
        self.w = IntVar()
        self.w_entry = Entry(frameParams,textvariable=self.w)
        self.w_entry.pack()
        self.w.set(3)

        self.text_q = Label(frameParams, text="Величина Q:")
        self.text_q.config(bg="white")
        self.text_q.pack()
        self.q = IntVar()
        self.q_entry = Entry(frameParams,textvariable=self.q)
        self.q_entry.pack()
        self.q.set(701)

        frameStartPlag = Frame(frameTools)
        frameStartPlag.pack()
        frameStartPlag.config(bg="white")
        self.languages = Listbox(frameStartPlag)
        self.languages.insert(0, *LANGUAGES)
        self.languages.pack()

        self.button_get_result = Button(frameStartPlag, text='Получить результат', font=("Arial Bold", 11),command=self.get_plag)
        self.button_get_result.pack()
       

        frame2 = Frame(self)
        frame2.pack()
        frame2.config(bg="white")

        self.result_analyzer = Text(frame2, width=int(100), height=int(100))
        self.result_analyzer.pack()
        self.result_analyzer.tag_config('warning', background="orange",)
        self.result_analyzer.tag_config('plag', background="red")
        



        

