'''
gptgui.py 2
    by Michael Leidel
remarks:
    Aug 2025
    Added 'temporaty conversation capability'
    added removed some options
    added speech toggle
    improved logging
'''
import os
import sys
import time
import configparser
import subprocess
import webbrowser
import markdown
import platform
import json
import openvoc
from tkinter.font import Font
from tkinter import messagebox
from tkinter import simpledialog
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from time import localtime, strftime
from openai import OpenAI


class Application(Frame):
    ''' main class docstring '''
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True, padx=4, pady=4)
        self.Saved = True
        self.cpath = "conversation.json"
        self.playback = False

        # get settings from ini file
        config = configparser.ConfigParser()
        config.read('gptgui.ini')
        self.MyTheme    = config['Main']['theme']
        self.MyPath     = config['Main']['path']
        self.MyFntQryF  = config['Main']['fontqryfam']
        self.MyFntQryZ  = config['Main']['fontqrysiz']
        self.MyFntGptF  = config['Main']['fontgptfam']
        self.MyFntGptZ  = config['Main']['fontgptsiz']
        self.MyModel    = config['Main']['engine']
        self.MyKey      = config['Main']['gptkey']
        self.MyEditor   = config['Main']['editor']
        self.MyFile     = config['Main']['tempfile']
        self.MyVoice    = config['Main']['voice']
        self.MyColor    = config['Main']['color']
        self.MySystem   = config['Main']['system']
        self.TOPFRAME   = int(config['Main']['top_frame'])
        # if len(self.MyKey) < 16:
        #     self.MyKey = os.environ.get(self.MyKey)  # Using ENV var instead of actual key string.

        self.intro = f'''
        Welcome to GptGUI 2
            a GUI desktop AI client for conversing with
            OpenAI's Large Language Models

        Model: {self.MyModel}
        role: {self.MySystem}
        qheight: {self.TOPFRAME}
        editor: {self.MyEditor}
        voice: {self.MyVoice}
        color: {self.MyColor}
        font1: {self.MyFntQryF}
        f1 size: {self.MyFntQryZ}
        font2: {self.MyFntGptF}
        f2 size: {self.MyFntGptZ}

        A registered OpenAI API key is required
        and set as a system environment variable

        Use Ctrl-H for list of keyboard commands
'''

        self.create_widgets()

    def create_widgets(self):
        ''' creates GUI for app '''
        # expand widget to fill the grid
        self.columnconfigure(1, weight=1, pad=5)
        self.columnconfigure(2, weight=1, pad=5)
        self.rowconfigure(2, weight=1, pad=5)

        self.query = Text(self)
        self.query.grid(row=1, column=1, columnspan=2, sticky='nsew')
        efont = Font(family=self.MyFntQryF, size=self.MyFntQryZ)
        self.query.configure(font=efont)
        self.query.config(wrap="word", # wrap=NONE
                          undo=True, # Tk 8.4
                          width=50,
                          height=self.TOPFRAME,
                          padx=5, # inner margin
                          #insertbackground='#000',   # cursor color
                          tabs=(efont.measure(' ' * 4),))

        self.scrolly = Scrollbar(self, orient=VERTICAL,
                                 command=self.query.yview)
        self.scrolly.grid(row=1, column=3, sticky='ns')  # use nse
        self.query['yscrollcommand'] = self.scrolly.set

        self.txt = Text(self)
        self.txt.grid(row=2, column=1, columnspan=2, sticky='nsew')
        efont = Font(family=self.MyFntGptF, size=self.MyFntGptZ)
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

        self.new = Button(btn_frame, text='New',
                            command=self.on_new,
                            bootstyle=(OUTLINE))
        self.new.grid(row=1, column=2, sticky='w',
                   pady=(5, 0), padx=(5, 7))

        self.view = Button(btn_frame, text='View',
                            command=self.on_view_file,
                            bootstyle=(OUTLINE))
        self.view.grid(row=1, column=4, sticky='w',
                   pady=(5, 0))

        self.purge = Button(btn_frame, text='Purge',
                            command=self.on_purge,
                            bootstyle=(OUTLINE))
        self.purge.grid(row=1, column=5, sticky='w',
                   pady=(5, 0), padx=5)

        self.open = Button(btn_frame, text='Text',
                            command=self.on_md_open,
                            bootstyle=(OUTLINE))
        self.open.grid(row=1, column=6, sticky='w',
                     pady=(5, 0), padx=5)

        self.md = Button(btn_frame, text='Html',
                            command=self.on_md_render,
                            bootstyle=(OUTLINE))
        self.md.grid(row=1, column=7, sticky='w',
                     pady=(5, 0), padx=(0, 5))

        self.opts = Button(btn_frame, text='Options',
                            command=self.options,
                            bootstyle=(OUTLINE))
        self.opts.grid(row=1, column=8, sticky='w',
                   pady=(5, 0), padx=5)

        self.sub = Button(btn_frame,
                            text='Submit Query (Ctrl-g)',
                            command=self.on_submit, width=20,
                            bootstyle=(OUTLINE))
        self.sub.grid(row=1, column=9, sticky='w',
                   pady=(5, 0), padx=(20, 0))

       # END BUTTON FRAME

        cls = Button(self, text='Close',
                    command=self.exit_program,
                    bootstyle=(OUTLINE))
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
        self.popup_query.add_separator()
        self.popup_query.add_command(label="Browser",
                                     command=lambda: self.popquery(6))
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
        root.bind("<Control-h>", self.on_kb_help)  # show hotkey help
        root.bind("<Control-q>", self.exit_program)  # Close button
        root.bind("<Control-g>", self.on_submit)  # Submit Query button
        root.bind("<Control-Return>", self.on_submit)  # Submit Query button
        root.bind("<Control-Shift-S>", self.speak_text)  # speak query response
        root.bind("<Control-Shift-T>", self.toggle_speech)  # on/off
        root.bind("<Control-f>", self.find_text)
        root.bind("<Control-n>", self.find_next)


        # ToolTips
        ToolTip(self.new,
                text="Start new conversation",
                bootstyle=(INFO, INVERSE),
                wraplength=140)
        ToolTip(self.view,
                text="View current log",
                bootstyle=(INFO, INVERSE),
                wraplength=140)
        ToolTip(self.purge,
                text="Delete current log",
                bootstyle=(INFO, INVERSE),
                wraplength=140)
        ToolTip(self.sub,
                text="Ctrl-Enter to Append",
                bootstyle=(INFO, INVERSE),
                wraplength=140)
        ToolTip(self.md,
                text="markdown to browser",
                bootstyle=(INFO, INVERSE),
                wraplength=140)
        ToolTip(self.open,
                text="markdown to text editor",
                bootstyle=(INFO, INVERSE),
                wraplength=140)



        self.txt.delete("1.0", END)
        self.txt.insert("1.0", self.intro)

        # Variable to store the current search term and the index of the last found match.
        self.search_term = None
        self.last_found_index = "1.0"

        # Create a tag to highlight the search result.
        self.txt.tag_config("highlight", background="gray", foreground="white")

        self.query.focus_set()

        #
        # on startup check for conversation.json file
        #

        self.conversation = self.load_buffer(self.cpath)

        if self.conversation == []:
            self.conversation = [
                {"role": "system", "content": self.MySystem}
            ]
            if os.path.isfile(self.cpath):
                os.remove(self.cpath)
        else:
            self.on_new()

        self.txt.tag_configure('all_text', foreground=self.MyColor)
        # use the following line to refresh the txt color when needed
        self.txt.tag_add('all_text', '1.0', 'end-1c')  # exclude trailing newline


#----------------------------------------------------------------------


    def on_submit(self, event=None):
        ''' Event handler for Submit button (Ctrl-G). '''
        self.txt.delete("1.0", END)
        self.txt.insert("1.0", "Thinking ..." )
        self.txt.update_idletasks()
        query = self.query.get("1.0", END)

        # 1) add the user message
        self.conversation.append(
            {"role": "user", "content": query}
        )

        # 2) call the chat completion
        ai_text, total, prompt, completion = self.gptCode(self.MyKey,
                                                          self.MyModel,
                                                          self.conversation)

        if ai_text == "":
            self.query.delete("1.0", END)
            self.txt.delete("1.0", END)
            self.txt.insert("1.0", self.intro)
            self.txt.tag_add('all_text', '1.0', 'end-1c')
            return

        # 3) add the assistant reply to history
        self.conversation.append(
            {"role": "assistant", "content": ai_text}
        )

        # 4) show it
        self.txt.delete("1.0", END)
        self.txt.insert("1.0", ai_text)
        self.txt.tag_add('all_text', '1.0', 'end-1c')

        # SAVE conversation to disk
        self.save_buffer(self.conversation, self.cpath)

        # append to log
        today = strftime("%a %d %b %Y", localtime())
        tm    = strftime("%H:%M", localtime())
        with open(self.MyPath, "a", encoding="utf-8") as fout:
            fout.write("\n\n=== Chat on %s %s ===\n\n" % (today, tm))
            fout.write(f"prompt:{prompt}, completion:{completion}, total:{total} \n\n")
            for msg in self.conversation:
                role = msg["role"]
                fout.write(f"{role.upper()}:\n{msg['content']}\n\n")
            fout.write("="*40 + "\n\n")

        # clear the input query box
        self.query.delete("1.0", END)
        self.query.focus_set()

        # Speak response, if speach is on ...
        if self.playback is True:
            self.speak_text(ai_text)


    def gptCode(self, key: str, model: str, messages: str) -> str:
        """Call the OpenAI ChatCompletion endpoint."""
        try:
            client = OpenAI(api_key=os.environ.get(key))
            resp = client.chat.completions.create(
            model    = model,
            messages = messages)
            content = resp.choices[0].message.content.strip()
            total_tokens, prompt_tokens, completion_tokens = self.extract_token_counts(resp)
            # Return as a tuple (content, total, prompt, completion)
            return content, total_tokens, prompt_tokens, completion_tokens
        except Exception as e:
            messagebox.showerror("Client Error", str(e))
            return ""

    def extract_token_counts(self, resp):
        """
        Return (total_tokens, prompt_tokens, completion_tokens)
        Works for both dict-like and object-like resp.
        """
        total_tokens = prompt_tokens = completion_tokens = None

        if isinstance(resp, dict):
            usage = resp.get('usage', {})
            total_tokens = usage.get('total_tokens')
            prompt_tokens = usage.get('prompt_tokens')
            completion_tokens = usage.get('completion_tokens')
        else:
            usage = getattr(resp, 'usage', None)
            if usage is not None:
                total_tokens = getattr(usage, 'total_tokens', None)
                prompt_tokens = getattr(usage, 'prompt_tokens', None)
                completion_tokens = getattr(usage, 'completion_tokens', None)

        return total_tokens, prompt_tokens, completion_tokens


    def on_purge(self):
        ''' User is purging the query-save file '''
        if not os.path.isfile(self.MyPath):
            messagebox.showwarning(self.MyPath, "Empty - No File to purge")
            return
        ret = messagebox.askokcancel("Purge", "Delete current log?")
        if ret is True:
            os.remove(self.MyPath)
            messagebox.showinfo("Purge", "Log Deleted.")


    def on_new(self):
        ''' Event handler for the New button.
        Optionally starts new conversation '''
        result = messagebox.askokcancel("Confirm New Conversation",
                                        "OK to start a new conversation?\nCANCEL to continue previous.")
        if result is True:
            # start new conversation
            self.conversation.clear()
            self.conversation = [
                {"role": "system", "content": self.MySystem}
            ]
            if os.path.isfile(self.cpath):
                os.remove(self.cpath)
            self.query.delete("1.0", END)
            self.txt.delete("1.0", END)
            self.txt.insert("1.0", self.intro)
            self.txt.tag_add('all_text', '1.0', 'end-1c')
        self.query.focus_set()


    def load_buffer(self, path):
        try:
            with open(self.cpath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # corrupted file -> start clean
            return []

    def save_buffer(self, buf, path):
        with open(self.cpath, "w", encoding="utf-8") as f:
            json.dump(buf, f, ensure_ascii=False, indent=2)

    def on_view_file(self):
        ''' View the user saved queries file. '''
        self.txt.delete("1.0", END)
        with open(self.MyPath, "r") as fin:
            self.txt.insert("1.0", fin.read())
        self.txt.see(END)
        self.query.delete("1.0", END)


    def options(self, e=None):
        ''' Launch Options program and exit this program '''
        if platform.system() == "Windows":
            subprocess.call(["pythonw.exe", "gptopt.py"])
        else:
            subprocess.call(["python3", "gptopt.py"])
        # re-read configuration
        config = configparser.ConfigParser()
        config.read('gptgui.ini')
        self.MyTheme = config['Main']['theme']
        self.MyPath = config['Main']['path']
        self.MyFntQryF = config['Main']['fontqryfam']
        self.MyFntQryZ = config['Main']['fontqrysiz']
        self.MyFntGptF = config['Main']['fontgptfam']
        self.MyFntGptZ = config['Main']['fontgptsiz']
        self.MyModel = config['Main']['engine']
        self.MyKey = config['Main']['gptkey']
        self.MyEditor = config['Main']['editor']
        self.MyFile = config['Main']['tempfile']
        self.MyVoice = config['Main']['voice']
        self.MySystem = config['Main']['system']
        self.TOPFRAME = int(config['Main']['top_frame'])
        # if len(self.MyKey) < 16:
        #     self.MyKey = os.environ.get(self.MyKey)  # Using ENV var instead of actual key string.
        # re-set the items and change font/size
        efont = Font(family=self.MyFntQryF, size=self.MyFntQryZ)
        self.query.configure(font=efont, height=self.TOPFRAME)
        efont = Font(family=self.MyFntGptF, size=self.MyFntGptZ)
        self.txt.configure(font=efont)
        style = Style()
        style = Style(theme=self.MyTheme)
        MyTitle = "GptGUI (OpenAI) " + self.MyModel
        root.title(MyTitle)


    def getmdtext(self):
        ''' get all or selected text '''
        if self.txt.tag_ranges("sel"):
            text = self.txt.selection_get()
        else:  # Select All
            self.txt.focus()
            self.txt.tag_add(SEL, '1.0', END)
            self.txt.mark_set(INSERT, '1.0')
            self.txt.see(INSERT)
            if self.txt.tag_ranges("sel"):
                text = self.txt.selection_get()
                self.txt.tag_remove(SEL, "1.0", END)
        return text


    def on_md_open(self, e=None):
        ''' open txt (MD) in your text editor '''
        text = self.getmdtext()
        filename = os.getcwd() + '/' + self.MyFile
        with open(filename, 'w') as f:
            f.write(text)
        print(self.MyEditor, filename)
        # subprocess.Popen([self.MyEditor, filename])
        os.system(self.MyEditor + " " + filename)


    def on_md_render(self, e=None):
        ''' render txt (MD) to html and show window '''
        text = self.getmdtext()
        # convert MD to HTML
        H = markdown.markdown(text,
                              extensions=['tables','fenced_code'])
        # write to file
        filename = os.getcwd() + '/' + self.MyFile + '.html'
        with open(filename, 'w') as f:
            f.write(H)
        # open file in browser
        webbrowser.open_new_tab('file:///' + filename)


    def toggle_speech(self, e=None):
        ''' Turn on/off auto play speech
        toggle voice playback of each response
        Requires mpv for Linux. Nothing for Windows. '''
        if self.playback == True:
            self.playback = False
            # announce it
            x = openvoc.textospeech(self.MyKey,
                                    self.MyVoice,
                                    'quickly',
                                    'speak.mp3',
                                    "Voice playback is now off.")
        else:
            self.playback = True
            # announce it
            x = openvoc.textospeech(self.MyKey,
                                    self.MyVoice,
                                    'quickly',
                                    'speak.mp3',
                                    "Voice playback is now on.")
        if x != 0:
            messagebox.showwarning("There is a problem with the toggle Speaking")


    def speak_text(self, e=None):
        ''' Speak the query response text
            key, voc, ins, fou, inp
        '''
        text = self.getmdtext()  # get selected or all text
        x = openvoc.textospeech(self.MyKey, self.MyVoice, 'normal', 'speech.mp3', text)
        if x != 0:
            messagebox.showerror("OpenVOC Error", "There is a problem with the voice file")


    def on_kb_help(self, e=None):
        ''' display hot keys message '''
        msg = '''
<Ctrl-h> HotKeys help
<Ctrl-g>      Submit Query
<Ctrl-Return> Submit Query
<Ctrl-q> Exit Program
<Ctrl-Shift-S> Speak the Text
<Ctrl-Shift-T> Toggle Speech
<Ctrl-f> Find Text
<Ctrl-n> Find Next Text
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
            self.TOPFRAME += 2
            self.query.config(height=self.TOPFRAME)
        elif n == 5:  # smaller
            if self.TOPFRAME > 3:
                self.TOPFRAME -= 2
                self.query.config(height=self.TOPFRAME)
        else:   # 6
            search = self.query.selection_get()
            webbrowser.open("https://duckduckgo.com/?q=" + search)

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

    def find_text(self, event=None):
        ''' Ask the user for the text to search
            then find and highlight the text if found.'''
        term = simpledialog.askstring("Find", "Enter text to search:")
        if term:
            self.search_term = term
            # Remove any previous highlights.
            self.txt.tag_remove("highlight", "1.0", tk.END)
            # Start searching from the beginning.
            self.last_found_index = "1.0"
            pos = self.txt.search(self.search_term, self.last_found_index, stopindex=tk.END)
            if pos:
                # Highlight the found text.
                end_pos = f"{pos}+{len(self.search_term)}c"
                self.txt.tag_add("highlight", pos, end_pos)
                # Adjust the view to make the found text visible.
                self.txt.see(pos)
                # Store the ending position for finding the next match.
                self.last_found_index = end_pos
            else:
                messagebox.showinfo("Result", "No matches found.")
        return "break"  # Prevent the default behavior.


    def find_next(self, event=None):
        ''' Search for next occurrence of text in response text area (self.txt) '''
        if not self.search_term:
            return self.find_text()

        pos = self.txt.search(self.search_term, self.last_found_index, stopindex=tk.END)
        if pos:
            # Remove previous highlights so only the current match is highlighted.
            self.txt.tag_remove("highlight", "1.0", tk.END)
            end_pos = f"{pos}+{len(self.search_term)}c"
            self.txt.tag_add("highlight", pos, end_pos)
            self.txt.see(pos)
            # Update the last found index.
            self.last_found_index = end_pos
        else:
            messagebox.showinfo("Result", "No more matches found.")
            self.txt.tag_remove("highlight", "1.0", tk.END)
        return "break"  # Prevent the default behavior.


    def exit_program(self, e=None):
        ''' Only exit program without prompt if
            1. Ctrl-q was hit
            OR
            2. Both Text frames are empty '''
        resp = self.txt.get("1.0", END).strip()
        qury = self.query.get("1.0", END).strip()
        if resp == "" and qury == "":
            save_location()
            sys.exit()
        if e is None:  # ctrl-q avoids this message
            if messagebox.askokcancel('GptGUI',
                                      'Confirm Exit app?') is False:
                return
        save_location()

#------------------------------------------------------------

# SAVE GEOMETRY INFO AND EXIT
def save_location(e=None):
    ''' executes at WM_DELETE_WINDOW event - see below
        Also called from self.exit_program.
        Save window geometry before destruction
    '''
    with open("winfo", "w") as fout:
        fout.write(root.geometry())
    root.destroy()

# get options that go into the window creation and title
config = configparser.ConfigParser()
config.read('gptgui.ini')
MyTheme = config['Main']['theme']
MyModel = config['Main']['engine']

# define main window
MyTitle = "GptGUI 2 " + MyModel
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
root.minsize(790, 325)  # width, height
Sizegrip(root).place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

Application(root)

root.mainloop()
