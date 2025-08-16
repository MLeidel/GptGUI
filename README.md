# GptGUI 2

### Python GUI to access Gpt Engine with OpenAI

-  Temporary Chat mode
-  supports a variety of OpenAI models
-  choose from many themes
-  convert responses to HTML or VOICE
-  maintains a log of reponses

see https://platform.openai.com/docs for model information

_make sure to pip install the latest **openai** module_  

----

## Instalation

For Linux / Mac you can either _gh repo clone MLeidel/GptGUI_ or download a zip
file of this repo.

Before using this application Python 3.x must be installed.

To install Python go to https://www.python.org/downloads/.  
Click __Download Python__ and follow the installation instructions.
`tkinter` is automatically installed with Python on Windows 
For Linux tkinter is installed with: `apt install python3-tk`

Use the requirements.txt file to install any modules you may be missing.
```bash
    pip3 install -r requirements.txt
```
**Voice**
For voice playback of the responses the `mpv` vidio player is required for Linux.  
For voice playback on Windows OS no player is required but VLC is recommended.

___

You will also have to Sign Up at https://openai.com/api/ and __create
an API Key__.  
There is no cost to do so.

___

After starting the app the first time click the _Options_
button.

Copy and past your API key into the "Gpt Key" entry box.  
A better way to handle your API key is to set it up as a System Environment Variable.  
Then put the variable's name into the "Gpt Key" entry box.

Change any other appearance or Gpt options as well.  

## gptgui.ini

The options are stored in a plain text file called _gptgui.ini_.  
If you prefer you could change the settings with a text editor.


![input box](images/gptopts.png "GptGUI options window")

---

## Buttons


![alttext](images/gptgui.png "Ctrl-t for Response Metrics")

Input your query in the top box, and hit __"Submit Query"__ or _Ctrl-g_.  
The Gpt AI response will appear in the larger box below.

**The buttons**:  

- New
> Begins a new conversation
- View
> Displays the log file you set up in Options  
- Purge
> Clears the contens of the log file  
- Text
> Opens the current response or selection in your text editor   
Set up the name of your text editor in the options.
- Html
> Opens the current response or selection in your default browser
Converting Markdown to HTML
- Options  
> launches the Options editor program
- Close
> Exit the program. _Ctrl-q_ exits the program quickly.

---

## Hot Keys

| key | action |
| :--- | :--- |
|__Ctrl-H__| This HotKey help|
|__Ctrl-Q__| Close Program No Prompt|
|__Ctrl-Shift-S__| Speak the Currrent Text|
|__Ctrl-Shift_T__| Toggle Speech|
|__Ctrl-G__| Submit Query (Button)|
|__Ctrl-Enter__ | same as Ctrl-g|
|__Ctrl-F__| Find text |
|__Ctrl-N__| Find next text |


---

### Context menu

There is a context (Right-Click) menu for convenience.
The height of the query text area (top frame) can be lengthened
or shortened with this menu.

----

END
