'''
code file: gptopt.py
comments:
    tkauto generated
'''
import os, sys
import configparser
from tkinter.font import Font
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Querybox
from tkinter import filedialog
from tkinter import messagebox

class Application(Frame):
    ''' main class docstring '''
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True, padx=4, pady=4)
        self.create_widgets()

    def create_widgets(self):
        ''' creates GUI for app '''
        lbl = Label(self, text='Theme')
        lbl.grid(row=1, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Path')
        lbl.grid(row=2, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Query Family')
        lbl.grid(row=3, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Query Size')
        lbl.grid(row=4, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Gpt Family')
        lbl.grid(row=5, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Gpt Size')
        lbl.grid(row=6, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Gpt Key')
        lbl.grid(row=7, column=1, sticky='e', pady=4, padx=4)

        self.vent_theme = StringVar()
        ent_theme = Combobox(self, textvariable=self.vent_theme, width=10)
        ent_theme['values'] = ('darkly', 'superhero', 'solar', 'cyborg', 'sandstone', 'yeti', 'pulse')
        # COMBO.bind('<<ComboboxSelected>>', self.ONCOMBOSELECT)
        ent_theme.current(0)
        ent_theme.grid(row=1, column=2, sticky='w', pady=4, padx=4)

        self.vent_path = StringVar()
        # self.vent_path.trace("w", self.eventHandler)
        ent_path = Entry(self, textvariable=self.vent_path, width=30)
        ent_path.grid(row=2, column=2, sticky='w', pady=4, padx=4)

        self.vent_fqfam = StringVar()
        # self.vent_fqfam.trace("w", self.eventHandler)
        ent_fqfam = Entry(self, textvariable=self.vent_fqfam, width=12)
        ent_fqfam.grid(row=3, column=2, sticky='w', pady=4, padx=4)

        self.vent_fqsiz = StringVar()
        # self.vent_fqsiz.trace("w", self.eventHandler)
        ent_fqsiz = Entry(self, textvariable=self.vent_fqsiz, width=2)
        ent_fqsiz.grid(row=4, column=2, sticky='w', pady=4, padx=4)

        self.vent_fgfam = StringVar()
        # self.vent_fgfam.trace("w", self.eventHandler)
        ent_fgfam = Entry(self, textvariable=self.vent_fgfam, width=12)
        ent_fgfam.grid(row=5, column=2, sticky='w', pady=4, padx=4)

        self.vent_fgsiz = StringVar()
        # self.vent_fgsiz.trace("w", self.eventHandler)
        ent_fgsiz = Entry(self, textvariable=self.vent_fgsiz, width=2)
        ent_fgsiz.grid(row=6, column=2, sticky='w', pady=4, padx=4)

        self.vent_gptkey = StringVar()
        # self.vent_gptkey.trace("w", self.eventHandler)
        ent_gptkey = Entry(self, textvariable=self.vent_gptkey, width=30)
        ent_gptkey.grid(row=7, column=2, sticky='w', pady=4, padx=4)

        btn_path = Button(self, text='Browse', command=self.browse_path)
        btn_path.grid(row=2, column=3, pady=4, padx=4)

        btn_qfont = Button(self, text='Choose', command=self.browse_font1)
        btn_qfont.grid(row=3, column=3, pady=4, padx=4)

        btn_gfont = Button(self, text='Choose', command=self.browse_font2)
        btn_gfont.grid(row=5, column=3, pady=4, padx=4)

        btn_close = Button(self, text='Save & Close', command=self.on_close)
        btn_close.grid(row=9, column=3, pady=4, padx=4)

        # set initial field values from ini file
        self.vent_theme.set(MyTheme)
        self.vent_path.set(MyPath)
        self.vent_fqfam.set(MyFntQryF)
        self.vent_fqsiz.set(MyFntQryZ)
        self.vent_fgfam.set(MyFntGptF)
        self.vent_fgsiz.set(MyFntGptZ)
        self.vent_gptkey.set(MyKey)

    def browse_path(self):
        ''' browse with filedialog for directory '''
        filename = filedialog.asksaveasfilename(initialdir = os.getcwd(),
                    title = "Select (create) Query-Save-File",
                    filetypes = (("text files","*.txt"),("all files","*.*")))
        if filename is not None:
            self.vent_path.set(filename)


    def browse_font1(self):
        ''' Get font & size for query text '''
        f = Querybox.get_font(parent=self)
        self.vent_fqfam.set(f.cget("family"))
        self.vent_fqsiz.set(str(f.cget("size")))

    def browse_font2(self):
        ''' Get font & size for Gpt text '''
        f = Querybox.get_font(parent=self)
        self.vent_fgfam.set(f.cget("family"))
        self.vent_fgsiz.set(str(f.cget("size")))


    def on_close(self):
        ''' Save to gptgui.ini and close the window '''
        config['Main']['fontqryfam'] = self.vent_fqfam.get()
        config['Main']['fontqrysiz'] = self.vent_fqsiz.get()
        config['Main']['fontgptfam'] = self.vent_fgfam.get()
        config['Main']['fontgptsiz'] = self.vent_fgsiz.get()
        config['Main']['gptkey'] = self.vent_gptkey.get()
        config['Main']['theme'] = self.vent_theme.get()
        config['Main']['path'] = self.vent_path.get()
        with open('gptgui.ini', 'w') as configfile:
            config.write(configfile)
        messagebox.showinfo("GptGUI Options",
                            "You will need to restart GptGUI before changes can take effect.")
        root.destroy()

    # def eventHandler(self):
    #     pass

    # def eventHandler(self):
    #     pass
#

config = configparser.ConfigParser()
config.read('gptgui.ini')

MyTheme = config['Main']['theme']
MyPath = config['Main']['path']
MyFntQryF = config['Main']['fontqryfam']
MyFntQryZ = config['Main']['fontqrysiz']
MyFntGptF = config['Main']['fontgptfam']
MyFntGptZ = config['Main']['fontgptsiz']
MyKey = config['Main']['gptkey']

# change working directory to path for this file
p = os.path.realpath(__file__)
os.chdir(os.path.dirname(p))

root = Window("GptGUI Options", MyTheme)

# root.protocol("WM_DELETE_WINDOW", save_location)  # UNCOMMENT TO SAVE GEOMETRY INFO
Sizegrip(root).place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
root.resizable(0, 0) # no resize & removes maximize button
# root.minsize(w, h)  # width, height
# root.maxsize(w, h)
# root.overrideredirect(True) # removed window decorations
root.iconphoto(False, PhotoImage(file='icon.png'))
root.attributes("-topmost", True)  # Keep on top of other windows

Application(root)

root.mainloop()
