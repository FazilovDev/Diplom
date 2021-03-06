import locale
from view.main_menu import MainMenu
from tkinter import *

def main():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF8')
    root = Tk()
    root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    app = MainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()

