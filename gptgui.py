'''
code file: gptgui.py
date: 1-31-2023
date: 2-07-2023 -> added result tokens messagebox
date: 2-08-2023 -> added time elapsed and title specs
date: 2-11-2023 -> added auto-save and context menus
'''
import os
import sys
import time
import configparser
import subprocess
from tkinter.font import Font
from tkinter import messagebox
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import datetime
import openai

# for subprocess to exec gptopt.py
PY = "python3"  # Linux
# PY = "pythonw"  # Windows

class Application(Frame):
    ''' main class docstring '''
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True, padx=4, pady=4)
        self.Saved = True
        self.create_widgets()

    def create_widgets(self):
        ''' creates GUI for app '''
        # expand widget to fill the grid
        self.columnconfigure(1, weight=1, pad=5)
        self.columnconfigure(2, weight=1, pad=5)
        self.rowconfigure(2, weight=1, pad=5)

        self.query = Text(self)
        self.query.grid(row=1, column=1, columnspan=2, sticky='nsew')
        efont = Font(family=MyFntQryF, size=MyFntQryZ)
        self.query.configure(font=efont)
        self.query.config(wrap="word", # wrap=NONE
                          undo=True, # Tk 8.4
                          width=50,
                          height=TOPFRAME,
                          padx=5, # inner margin
                          #insertbackground='#000',   # cursor color
                          tabs=(efont.measure(' ' * 4),))

        self.scrolly = Scrollbar(self, orient=VERTICAL,
                                 command=self.query.yview)
        self.scrolly.grid(row=1, column=3, sticky='ns')  # use nse
        self.query['yscrollcommand'] = self.scrolly.set

        self.txt = Text(self)
        self.txt.grid(row=2, column=1, columnspan=2, sticky='nsew')
        efont = Font(family=MyFntGptF, size=MyFntGptZ)
        self.txt.configure(font=efont)
        self.txt.config(wrap="word", # wrap=NONE
                        undo=True, # Tk 8.4
                        width=50,
                        height=12,
                        padx=5, # inner margin
                        #insertbackground='#000',   # cursor color
                        tabs=(efont.measure(' ' * 4),))

        self.scrolly = Scrollbar(self, orient=VERTICAL, command=self.txt.yview)
        self.scrolly.grid(row=2, column=3, sticky='ns')  # use nse
        self.txt['yscrollcommand'] = self.scrolly.set

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
        opts = Button(btn_frame, text='Options', command=self.options)
        opts.grid(row=1, column=6, sticky='w',
                   pady=(5, 0), padx=5)
        self.sub = Button(btn_frame,
                     text='Submit Query',
                     command=self.on_submit, width=35)
        self.sub.grid(row=1, column=7, sticky='w',
                   pady=(5, 0), padx=(20, 0))

       # END BUTTON FRAME

        cls = Button(self, text='Close', command=save_location)
        cls.grid(row=4, column=2, columnspan=2, sticky='e',
                 pady=(5,0), padx=5)

        # Popup menus - for self.query Text widgets
        self.popup_query = Menu(tearoff=0, title="title")
        self.popup_query.add_command(label="Copy",
                               command=lambda: self.popquery(1))
        self.popup_query.add_command(label="Paste",
                               command=lambda: self.popquery(2))
        self.popup_query.add_separator()
        self.popup_query.add_command(label="Copy All",
                                     command=lambda: self.popquery(3))
        self.popup_query.add_separator()
        self.popup_query.add_command(label="Larger",
                                     command=lambda: self.popquery(4))
        self.popup_query.add_command(label="Smaller",
                                     command=lambda: self.popquery(5))
        self.query.bind("<Button-3>", self.do_pop_query)
        # Popup menus - for self.txt Text widgets
        self.popup_txt = Menu(tearoff=0, title="title")
        self.popup_txt.add_command(label="Copy",
                               command=lambda: self.poptxt(1))
        self.popup_txt.add_command(label="Paste",
                               command=lambda: self.poptxt(2))
        self.popup_txt.add_separator()
        self.popup_txt.add_command(label="Copy All",
                                     command=lambda: self.poptxt(3))
        self.txt.bind("<Button-3>", self.do_pop_txt)


        # Bindings
        root.bind("<Control-t>", self.show_tokens)  # Show result tokens in title
        root.bind("<Control-m>", self.on_toggle_time)  # time elapsed toggle
        root.bind("<Control-h>", self.on_kb_help)  # show hotkey help
        root.bind("<Control-k>", self.options)  # Options button
        root.bind("<Control-q>", save_location)  # Close button
        root.bind("<Control-s>", self.on_save_file)  # Save button
        root.bind("<Control-g>", self.on_submit)  # Submit Query button

        # ToolTips
        ToolTip(self.query,
                text="Type your query here. Then hit 'Submit Query",
                bootstyle=(INFO))
        ToolTip(purge,
                text="Remove all saved query responses",
                bootstyle=(INFO))

        if MySave == "1":
            self.save.config(text="Auto Save", bootstyle="default-outline")
        self.query.focus_set()

#       check if query entered on command line
#       if it query entered on command line
#       then execute it immediately
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            self.query.insert("1.0", query)
            self.on_submit()

#----------------------------------------------------------------------

    def on_submit(self, e=None):
        ''' Query OpenAI Gpt engine and display response in Text widgit'''
        start = time.time()  # time the Gpt retrival
        querytext = self.query.get("1.0", END)
        if len(querytext) < 4:
            return
        if MySave == "0":
            self.save.configure(bootstyle=DEFAULT) # new - not been saved
            self.Saved = False
        # get the Gpt key from the ini value
        try:
            openai.api_key = MyKey
        except Exception as e:
            messagebox.showerror("Could Not Read Key file",
                       "Did you enter your Gpt Key?")
            return
        # may take some time
        # things are locked up until response returns
        try:
            response = openai.Completion.create(
            model=MyModel,
            prompt=querytext.strip(),
            temperature=float(MyTemp),
            max_tokens=int(MyTokens),
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)
            # display Gpt response in Text widget
            output = response["choices"][0]["text"]
            # collect response token info
            self.length = len(output)
            self.completion = response["usage"]["completion_tokens"]
            self.total = response["usage"]["total_tokens"]
            self.prompt = response["usage"]["prompt_tokens"]
            # display response text
            if MyTime == "1":
                self.elapsed = (time.time() - start)
                output = f"elapsed time: {round(self.elapsed, 5)}\n-----" + output
            self.txt.delete("1.0", END)
            self.txt.insert("1.0", output)
            # on Auto Save do the save
            if MySave == "1":
                self.on_save_file()
        except Exception as e:
            messagebox.showerror("Problems", e)

    def on_purge(self):
        ''' User is purging the query-save file '''
        if not os.path.isfile(MyPath):
            messagebox.showwarning(MyPath, "Empty - No File to purge")
            return
        ret = messagebox.askokcancel("Purge", "Delete All Saved Queries?")
        if ret is True:
            os.remove(MyPath)
            messagebox.showinfo("Purge", "Saved Queries Deleted.")


    def on_clear_all(self):
        ''' User is clearning the GUI fields '''
        if self.Saved is False:
            if messagebox.askokcancel('GptGUI',
                                      'Last response not saved - continue?') is False:
                return

        self.txt.delete("1.0", END)
        self.query.delete("1.0", END)
        self.save.configure(bootstyle=DEFAULT) # new - not been saved
        self.Saved = True


    def on_save_file(self, e=None):
        ''' Save the current query and result to user file (MyPath) '''
        resp = self.txt.get("1.0", END).strip()
        qury = self.query.get("1.0", END).strip()
        if qury == "" or resp == "":  # make sure there is a query present
            return
        try:
            msg = "\ncompletion tokens: " + str(self.completion) + \
                  "\ntotal tokens: " + str(self.total) + \
                  "\nprompt tokens: " + str(self.prompt) + "\n-----\n"
            with open(MyPath, "a") as fout:
                fout.write(str(now.strftime("%Y-%m-%d %H:%M\n")))
                fout.write(qury + "\n----- " + MyModel)
                fout.write(msg)
                fout.write(resp.strip() + "\n----------------\n\n")
        except Exception as e:
            messagebox.showerror("Save Query Problem", e)

        if MySave == "0":  # Auto Save is off
            # indicate that a "save" has processed
            self.save.configure(bootstyle="default-outline")
            self.Saved = True


    def on_view_file(self):
        ''' View the user saved queries file '''
        if not os.path.isfile(MyPath):
            messagebox.showwarning(MyPath, "Empty - No File")
            return
        if self.Saved is False:
            if messagebox.askokcancel('GptGUI',
                                      'Last response not saved - continue?') is False:
                return
        # Either the user has or has-not saved the current query reponse.
        # Therefore, set the "Save" button back to DEFAULT because
        # if the response was not saved prior, then it is just lost.
        self.Saved = True
        self.save.configure(bootstyle=DEFAULT)
        self.txt.delete("1.0", END)
        with open(MyPath, "r") as fin:
            self.txt.insert("1.0", fin.read())
        self.query.delete("1.0", END)


    def options(self, e=None):
        # os.system("python3 gptopt.py") # not work well with Windows
        subprocess.Popen([PY, "gptopt.py"])

    def show_tokens(self, e=None):
        ''' show response tokens '''
        msg = "text length: " + str(self.length) + \
              "\ncompletion tokens: " + str(self.completion) + \
              "\ntotal tokens: " + str(self.total) + \
              "\nprompt tokens: " + str(self.prompt) + \
              "\nResponse Time Elapsed: " + str(self.elapsed)
        messagebox.showinfo("GptGUI Response Tokens", msg)

    def on_toggle_time(self, e=None):
        global MyTime
        if MyTime == "1":
            MyTime = "0"
        else:
            MyTime = "1"
        messagebox.showinfo("Toggle Show Elapsed Time",
                            "    Set to " + MyTime + "       ")

    def on_kb_help(self, e=None):
        msg = '''
<Control-t> View response metrics\n
<Control-m> Toggle elapsed time in output\n
            (Does not effect Options flag)
<Control-h> This HotKey help\n
<Control-k> Set Options (Button)\n
<Control-q> Close Program (Button)\n
<Control-s> Save output (Button)\n
<Control-g> Submit Query (Button)\n
        '''
        messagebox.showinfo("Hot Keys Help", msg)


    def do_pop_query(self, event):
        ''' handles right-click for context menu '''
        try:
            self.popup_query.tk_popup(event.x_root,
                                event.y_root, 0)
        except:
            self.popup_query.grab_release()

    def do_pop_txt(self, event):
        ''' handles right-click for context menu '''
        try:
            self.popup_txt.tk_popup(event.x_root,
                                event.y_root, 0)
        except:
            self.popup_txt.grab_release()

    def popquery(self, n):
        ''' Routes query Text context menu actions '''
        global TOPFRAME
        if n == 1:  # Copy
            root.clipboard_clear()  # clear clipboard contents
            if self.query.tag_ranges("sel"):
                root.clipboard_append(self.query.selection_get())  # append new value to clipbaord
        elif n == 2:  # Paste
            inx = self.query.index(INSERT)
            try:
                self.query.insert(inx, root.clipboard_get())
            except Exception as e:
                return
        elif n == 3:  # Copy All
            self.query.focus()
            self.query.tag_add(SEL, '1.0', END)
            self.query.mark_set(INSERT, '1.0')
            self.query.see(INSERT)
            root.clipboard_clear()  # clear clipboard contents
            if self.query.tag_ranges("sel"):  # append new value to clipbaord
                root.clipboard_append(self.query.selection_get())
                self.query.tag_remove(SEL, "1.0", END)
        elif n == 4:  # larger
            TOPFRAME += 2
            self.query.config(height=TOPFRAME)
        elif n == 5:  # smaller
            if TOPFRAME > 3:
                TOPFRAME -= 2
                self.query.config(height=TOPFRAME)

    def poptxt(self, n):
        ''' Routes txt Text context menu actions '''
        if n == 1:  # Copy
            root.clipboard_clear()  # clear clipboard contents
            root.clipboard_append(self.txt.selection_get())  # append new value to clipbaord
        elif n == 2:  # Paste
            inx = self.txt.index(INSERT)
            self.txt.insert(inx, root.clipboard_get())
        else:  # Select All
            self.txt.focus()
            self.txt.tag_add(SEL, '1.0', END)
            self.txt.mark_set(INSERT, '1.0')
            self.txt.see(INSERT)
            root.clipboard_clear()  # clear clipboard contents
            if self.txt.tag_ranges("sel"):  # append new value to clipbaord
                root.clipboard_append(self.txt.selection_get())
                self.txt.tag_remove(SEL, "1.0", END)

#------------------------------------------------------------

# SAVE GEOMETRY INFO AND EXIT
def save_location(e=None):
    ''' executes at WM_DELETE_WINDOW event - see below '''
    if messagebox.askokcancel('GptGUI',
                           'Did you want to close the app?') is False:
        return
    with open("winfo", "w") as fout:
        fout.write(root.geometry())
    root.destroy()

# used for saving queries with date and time
now = datetime.datetime.now()

# get settings from ini file
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
MyKey = config['Main']['gptkey']  # can be actual key or ENV var.
MyTime = config['Main']['showtime']
MySave = config['Main']['autosave']
TOPFRAME = int(config['Main']['top_frame'])
if len(MyKey) < 16:
    MyKey = os.environ.get(MyKey)  # Using ENV var instead of actual key string.


# define main window
MyTitle = "GptGUI (OpenAI) " + MyModel + " " + str(MyTokens) + " " + str(MyTemp)
root = Window(MyTitle, MyTheme, iconphoto="icon.png")

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
root.minsize(768, 325)  # width, height
Sizegrip(root).place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

Application(root)

root.mainloop()
