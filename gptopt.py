'''
code file: gptopt.py
3-15-23 - Add gpt-3.5-turbo
'''
import os, sys
import configparser
import subprocess
from tkinter.font import Font
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Querybox
from tkinter import filedialog
from tkinter import messagebox

## for subprocess to exec gptopt.py
PY = "python3"  # Linux
GPTGUI = "gptgui.py"
# PY = "pythonw"  # Windows
# GPTGUI = "gptgui.pyw"

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

        lbl = Label(self, text='Save File Path')
        lbl.grid(row=2, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Query Family')
        lbl.grid(row=3, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Query Size')
        lbl.grid(row=4, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Gpt Family')
        lbl.grid(row=5, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Font Gpt Size')
        lbl.grid(row=6, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Engine')
        lbl.grid(row=7, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Temperature')
        lbl.grid(row=8, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Tokens')
        lbl.grid(row=9, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Gpt Key')
        lbl.grid(row=10, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Time Elapsed')
        lbl.grid(row=11, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Auto Save')
        lbl.grid(row=12, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Top Frame Size')
        lbl.grid(row=13, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Text editor')
        lbl.grid(row=14, column=1, sticky='e', pady=4, padx=4)

        lbl = Label(self, text='Temp file name')
        lbl.grid(row=15, column=1, sticky='e', pady=4, padx=4)

        self.vent_theme = StringVar()
        ent_theme = Combobox(self, textvariable=self.vent_theme, width=10)
        ent_theme['values'] = ('darkly',
                               'superhero',
                               'solar',
                               'cyborg',
                               'sandstone',
                               'yeti',
                               'pulse',
                               'cosmo',
                               'flatly',
                               'litera',
                               'minty',
                               'lumen',
                               'journal',
                               'simplex',
                               'cerculean')
        ent_theme.current(0)
        ent_theme.grid(row=1, column=2, sticky='w', pady=4, padx=4)

        self.vent_path = StringVar()
        ent_path = Entry(self, textvariable=self.vent_path, width=30)
        ent_path.grid(row=2, column=2, sticky='w', pady=4, padx=4)

        self.vent_fqfam = StringVar()
        ent_fqfam = Entry(self, textvariable=self.vent_fqfam, width=12)
        ent_fqfam.grid(row=3, column=2, sticky='w', pady=4, padx=4)

        self.vent_fqsiz = StringVar()
        ent_fqsiz = Entry(self, textvariable=self.vent_fqsiz, width=3)
        ent_fqsiz.grid(row=4, column=2, sticky='w', pady=4, padx=4)

        self.vent_fgfam = StringVar()
        ent_fgfam = Entry(self, textvariable=self.vent_fgfam, width=12)
        ent_fgfam.grid(row=5, column=2, sticky='w', pady=4, padx=4)

        self.vent_fgsiz = StringVar()
        ent_fgsiz = Entry(self, textvariable=self.vent_fgsiz, width=3)
        ent_fgsiz.grid(row=6, column=2, sticky='w', pady=4, padx=4)

        self.vcmbo_model = StringVar()
        cmbo_model = Combobox(self, textvariable=self.vcmbo_model, width=20)
        cmbo_model['values'] = ('gpt-4o',
                                'gpt-4-turbo',
                                'gpt-4',
                                'gpt-3.5-turbo')

        # ent_model.current(0)
        cmbo_model.grid(row=7, column=2, sticky='w', pady=4, padx=4)
        cmbo_model.bind('<<ComboboxSelected>>', self.onComboSelect)

        self.vcmbo_temp = StringVar()
        cmbo_temp = Combobox(self, textvariable=self.vcmbo_temp, width=6)
        cmbo_temp['values'] = ('0.7', '0.8', '0.9', '1.0', '1.2')
        # COMBO.bind('<<ComboboxSelected>>', self.ONCOMBOSELECT)
        # ent_model.current(0)
        cmbo_temp.grid(row=8, column=2, sticky='w', pady=4, padx=4)

        self.vent_token = StringVar()
        ent_token = Entry(self, textvariable=self.vent_token, width=6)
        ent_token.grid(row=9, column=2, sticky='w', pady=4, padx=4)

        self.vent_gptkey = StringVar()
        # self.vent_gptkey.trace("w", self.eventHandler)
        self.ent_gptkey = Entry(self, textvariable=self.vent_gptkey, width=30)
        self.ent_gptkey.grid(row=10, column=2, sticky='w', pady=4, padx=4)

        self.vcb = IntVar()
        cb = Checkbutton(self, variable=self.vcb, text='Check to show in output')
        cb.grid(row=11, column=2, sticky=W, padx=5, pady=5)

        self.vcv = IntVar()
        cb = Checkbutton(self, variable=self.vcv, text='Check to turn on')
        cb.grid(row=12, column=2, sticky=W, padx=5, pady=5)

        self.vent_size = StringVar()
        ent_size = Entry(self, textvariable=self.vent_size, width=4)
        ent_size.grid(row=13, column=2, sticky='w', pady=4, padx=4)

        self.vent_edit = StringVar()
        ent_edit = Entry(self, textvariable=self.vent_edit)
        ent_edit.grid(row=14, column=2, sticky='w', pady=4, padx=4)

        self.vent_file = StringVar()
        end_file = Entry(self, textvariable=self.vent_file)
        end_file.grid(row=15, column=2, sticky='w', pady=4, padx=4)

        btn_path = Button(self, text='Browse', command=self.browse_path)
        btn_path.grid(row=2, column=3, pady=4, padx=4)

        btn_qfont = Button(self, text='Choose', command=self.browse_font1)
        btn_qfont.grid(row=3, column=3, pady=4, padx=4)

        btn_gfont = Button(self, text='Choose', command=self.browse_font2)
        btn_gfont.grid(row=5, column=3, pady=4, padx=4)

        btn_close = Button(self, text='Save & Close', command=self.on_close)
        btn_close.grid(row=15, column=3, pady=4, padx=4)

        # set initial field values from ini file
        self.vent_theme.set(MyTheme)
        self.vent_path.set(MyPath)
        self.vent_fqfam.set(MyFntQryF)
        self.vent_fqsiz.set(MyFntQryZ)
        self.vent_fgfam.set(MyFntGptF)
        self.vent_fgsiz.set(MyFntGptZ)
        self.vent_gptkey.set(MyKey)
        self.vcmbo_model.set(MyModel)
        self.vcmbo_temp.set(MyTemp)
        self.vent_token.set(MyTokens)
        self.vcb.set(MyTime)
        self.vcv.set(MySave)
        self.vent_size.set(MySize)
        self.vent_edit.set(MyEditor)
        self.vent_file.set(MyFile)

        ToolTip(self.ent_gptkey,
                text="Env Var or Key Literal",
                bootstyle=(INFO, INVERSE),
                wraplength=140)


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

    def onComboSelect(self, e):
        ''' pre set the tokens field for model '''
        tok = self.vcmbo_model.get()
        if tok == "gpt-3.5-turbo" :
            self.vent_token.set("4097")
        elif tok == "gpt-3.5-turbo-16k" :
            self.vent_token.set("16385")

    def on_close(self):
        ''' Save to gptgui.ini and close the window '''
        config['Main']['fontqryfam'] = self.vent_fqfam.get()
        config['Main']['fontqrysiz'] = self.vent_fqsiz.get()
        config['Main']['fontgptfam'] = self.vent_fgfam.get()
        config['Main']['fontgptsiz'] = self.vent_fgsiz.get()
        config['Main']['gptkey'] = self.vent_gptkey.get().strip()
        config['Main']['theme'] = self.vent_theme.get()
        config['Main']['path'] = self.vent_path.get()
        config['Main']['engine'] = self.vcmbo_model.get()
        config['Main']['temperature'] = self.vcmbo_temp.get()
        config['Main']['tokens'] = self.vent_token.get()
        config['Main']['showtime'] = str(self.vcb.get())
        config['Main']['autosave'] = str(self.vcv.get())
        config['Main']['top_frame'] = str(self.vent_size.get())
        config['Main']['editor'] = str(self.vent_edit.get())
        config['Main']['tempfile'] = str(self.vent_file.get())

        with open('gptgui.ini', 'w') as configfile:
            config.write(configfile)
        root.destroy()


config = configparser.ConfigParser()
config.read('gptgui.ini')

MyTheme = config['Main']['theme']
MyPath = config['Main']['path']
MyFntQryF = config['Main']['fontqryfam']
MyFntQryZ = config['Main']['fontqrysiz']
MyFntGptF = config['Main']['fontgptfam']
MyFntGptZ = config['Main']['fontgptsiz']
MyModel = config['Main']['engine']
MyTemp = config['Main']['temperature']
MyTokens = config['Main']['tokens']
MyKey = config['Main']['gptkey']
MyTime = config['Main']['showtime']
MySave = config['Main']['autosave']
MySize = config['Main']['top_frame']
MyEditor = config['Main']['editor']
MyFile = config['Main']['tempfile']

# change working directory to path for this file
p = os.path.realpath(__file__)
os.chdir(os.path.dirname(p))

root = Window("GptGUI Options", MyTheme)

Sizegrip(root).place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
root.resizable(0, 0) # no resize & removes maximize button
root.iconphoto(False, PhotoImage(file='icon.png'))
root.attributes("-topmost", True)  # Keep on top of other windows
# root.geometry("+100+20")
Application(root)

root.mainloop()
