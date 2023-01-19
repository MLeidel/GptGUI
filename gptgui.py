'''
code file: gptgui.py
date: 1-13-2023
'''
import openai
import os, sys
from tkinter.font import Font
from ttkbootstrap import *
from ttkbootstrap.constants import *
import pyperclip as pyc
import datetime
from tkinter import messagebox

# This is my module to read and return ini file key values
# Keys are case-sensitive
def striplist(lst):
    ''' strip items in a list and return list '''
    L = [i.strip() for i in lst]
    return L

def ini_read(inifile, *keys):
    ''' Open and read text file having "key = value" lines
        Build a dictionary - use it to build a list of
        values to return in the order received.
    '''

    kv = []  # one key/value item from ini file

    kvs = {}  # key/value dictionary built from ini file

    rtv = []  # return values stored here in kargs order

    with open(inifile) as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            if line.startswith('#'):
                continue
            # Build dictionary line by line from ini file
            kv = line.split('=')
            kv = striplist(kv)
            kvs[kv[0]] = kv[1]  # add to dictionary

    # Append requested key values and return list
    for v in keys:
        try:
            rtv.append(kvs[v])
        except:
            print("ini - Key Error or not used:", v)
            rtv.append(0)

    return rtv

# ----------------------------------------------------------------

class Application(Frame):
    ''' main class docstring '''
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True, padx=4, pady=4)
        self.create_widgets()

    def create_widgets(self):
        ''' creates GUI for app '''
        # expand widget to fill the grid
        self.columnconfigure(1, weight=1, pad=5)
        self.columnconfigure(2, weight=1, pad=5)
        self.rowconfigure(2, weight=1, pad=5)

        ''' ONLY OPTIONS FOR 'grid' FUNCTIONS:
                column  row
                columnspan  rowspan
                ipadx and ipady
                padx and pady
                sticky="nsew"
        --------------------------------------'''

        self.ventry = StringVar()
        self.query = Entry(self, textvariable=self.ventry)
        self.query.grid(row=1, column=1, columnspan=2, sticky='ew')

        self.sub = Button(self, text='Query', command=self.on_submit)
        self.sub.grid(row=1, column=2, columnspan=2, sticky='e', pady=5)

        self.txt = Text(self)
        self.txt.grid(row=2, column=1, columnspan=2, sticky='nsew')
        efont = Font(family="Consolas", size=12)
        self.txt.configure(font=efont)
        self.txt.config(wrap="word", # wrap=NONE
                           undo=True, # Tk 8.4
                           width=50,
                           height=12,
                           padx=5, # inner margin
                           insertbackground='#000',   # cursor color
                           tabs=(efont.measure(' ' * 4),))
        self.txt.focus()
        ## basic handler commands #
        # .get("1.0", END)
        # .delete("1.0", END)
        # .insert("1.0", "New text content ...")
        

        self.scrolly = Scrollbar(self, orient=VERTICAL, command=self.txt.yview)
        self.scrolly.grid(row=2, column=3, sticky='ns')  # use nse
        self.txt['yscrollcommand'] = self.scrolly.set
        # DON'T NEED HORZ SCROLLING
        # self.scrollx = Scrollbar(self, orient=HORIZONTAL, command=self.txt.xview)
        # self.scrollx.grid(row=3, column=1, columnspan=2, sticky='ew')
        # self.txt['xscrollcommand'] = self.scrollx.set

        # BUTTON FRAME
        btn_frame = Frame(self)
        btn_frame.grid(row=4, column=1, sticky='w')

        clear = Button(btn_frame, text='Clear', command=self.on_clear_all)
        clear.grid(row=1, column=2, sticky='w',
                   pady=(5, 0), padx=(5, 7))
        self.save = Button(btn_frame, text='Save', command=self.on_save_file)
        self.save.grid(row=1, column=3, sticky='w',
                   pady=(5, 0), padx=5)
        view = Button(btn_frame, text='View', command=self.on_view_file)
        view.grid(row=1, column=4, sticky='w',
                   pady=(5, 0))
        purge = Button(btn_frame, text='Purge', command=self.on_purge)
        purge.grid(row=1, column=5, sticky='w',
                   pady=(5, 0), padx=5)
       # END BUTTON FRAME

        cls = Button(self, text='Close', command=save_location)
        cls.grid(row=4, column=2, columnspan=2, sticky='e',
                 pady=(5,0), padx=5)

        self.query.bind("<Return>", self.on_submit)
        self.query.focus_set()


    def on_submit(self, e=None):
        ''' Query OpenAI Gpt engine and display response in Text widgit'''
        querytext = self.ventry.get()
        if len(querytext) < 4:
            return
        self.save.configure(bootstyle="default") # new - not been saved
        # User can store the GPTKEY in the gptgui.ini file
        # or set it in env variable GPTKEY
        if GptKey == 0:
            openai.api_key = os.getenv("GPTKEY")
        else:
            openai.api_key = GptKey
        # print(querytext)
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=querytext.strip(),
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
        output = response["choices"][0]["text"]
        self.txt.delete("1.0", END)
        self.txt.insert("1.0", output)


    # def on_copy(self):
    #     ''' Copy all Text to clipboard '''
    #     self.txt.tag_add(SEL, '1.0', END)
    #     self.txt.mark_set(INSERT, '1.0')
    #     self.txt.see(INSERT)
    #     if self.txt.tag_ranges("sel"):
    #         pyc.copy(self.txt.selection_get())
    #         self.txt.tag_remove("sel", "1.0", END)


    def on_purge(self):
        if not os.path.isfile(MyPath):
            messagebox.showwarning(MyPath, "Empty - No File to purge")
            return
        ret = messagebox.askokcancel("Purge", "Delete All Saved Queries?")
        if ret is True:
            os.remove(MyPath)
            messagebox.showinfo("Purge", "Saved Queries Deleted.")


    def on_clear_all(self):
        self.txt.delete("1.0", END)
        self.ventry.set("")


    def on_save_file(self):
        ''' Save the current query and result to user file (MyPath) '''
        resp = self.txt.get("1.0", END).strip()
        qury = self.ventry.get().strip()
        if qury == "" or resp == "":  # make sure there is a query present
            return
        with open(MyPath, "a") as fout:
            fout.write(str(now.strftime("%Y-%m-%d %H:%M\n")))
            fout.write(qury + "\n-----\n")
            fout.write(resp.strip() + "\n----------------\n\n")
        # indicate that a "save" has processed
        self.save.configure(bootstyle="default-outline")


    def on_view_file(self):
        ''' View the user saved queries file '''
        if not os.path.isfile(MyPath):
            messagebox.showwarning(MyPath, "Empty - No File")
            return
        self.txt.delete("1.0", END)
        with open(MyPath, "r") as fin:
            self.txt.insert("1.0", fin.read())
        self.ventry.set("")


# SAVE GEOMETRY INFO AND EXIT
def save_location(e=None):
    ''' executes at WM_DELETE_WINDOW event - see below '''
    with open("winfo", "w") as fout:
        fout.write(root.geometry())
    root.destroy()


now = datetime.datetime.now()

MyTheme, MyPath, GptKey = ini_read("gptgui.ini",
                                'theme',
                                'path',
                                'gptkey')
#print("gptkey=", GptKey)

root = Window("GptGUI", MyTheme)

# change working directory to path for this file
p = os.path.realpath(__file__)
os.chdir(os.path.dirname(p))

# ACCESS GEOMETRY INFO
if os.path.isfile("winfo"):
    with open("winfo") as f:
        lcoor = f.read()
    root.geometry(lcoor.strip())
else:
    root.geometry("675x505") # WxH+left+top

root.protocol("WM_DELETE_WINDOW", save_location)  # TO SAVE GEOMETRY INFO
Sizegrip(root).place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

Application(root)

root.mainloop()
