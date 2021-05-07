from tkinter import *
from view.moss_algorithm_menu import *
from view.ast_algorithm_menu import *
from threading import Thread

class MainMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.parent.title("DetectPlagiarism")
        self.pack(fill=BOTH, expand=True)

        self.tool_bar = None
        self.top_frame = None
        self.algorithm_plagiarizm = None

        self.view_menu()

    def view_tool_bar(self):
        self.tool_bar = Frame(self)
        self.tool_bar.pack()
        self.exit_button = Button(self.tool_bar, text="В главное меню", font=("Arial Bold", 14), command=self.close_moss_algorithm)
        self.exit_button.config(bg="white")
        self.exit_button.pack()

    def view_menu(self):
        self.top_frame = Frame(self)
        self.top_frame.pack(fill=X)
        self.top_frame.config(bg="white")

        self.algorithms_text = Label(self.top_frame, text="Выберите алгоритм:", font=("Arial Bold", 28))
        self.algorithms_text.config(bg="white")
        self.algorithms_text.pack()

        self.moss_algorithm_button = Button(self.top_frame, text="Алгоритм Moss", font=("Arial Bold", 14), command=self.go_to_moss_algorithm)
        self.moss_algorithm_button.pack()
        
        self.moss_algorithm_button = Button(self.top_frame, text="Алгоритм Ast", font=("Arial Bold", 14), command=self.go_to_ast_algorithm)
        self.moss_algorithm_button.pack()
    
    
    def close_menu(self):
        self.top_frame.destroy()
        self.view_tool_bar()

    def go_to_moss_algorithm(self):
        self.close_menu()
        self.algorithm_plagiarizm = MossAlgorithmMenu(self)
        self.algorithm_plagiarizm.open()

    def close_moss_algorithm(self):
        self.algorithm_plagiarizm.close()
        self.tool_bar.destroy()
        self.view_menu()

    def go_to_ast_algorithm(self):
        self.close_menu()
        self.algorithm_plagiarizm = AstAlgorithmMenu(self)
        self.algorithm_plagiarizm.open()



    