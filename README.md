# GptGUI
_Python GUI for Linux or Windows to access OpenAI Gpt Engine._

## Instalation

For windows you can downolad the setup_GptGUI.exe file supplied with this repo.

For Linux / Mac you can either _gh repo clone MLeidel/GptGUI_ or download a zip
file of this repo.


Before using this application Python 3.x must be installed.

To install Python go to https://www.python.org/downloads/.  
Click __Download Python 3.???__ and follow the installation instructions.

You will also have to Sign Up at https://openai.com/api/ and __create
anAPI Key__.  
There is no cost to do so.

### _There are two options to apply your key to the program_.  
### The first option is to set the GPTKEY as an environment variable.  
#### For Windows:  
Set a Windows _system environment variable_ to add your OpenAI KEY.  
To do this go to the start menu and begin typing "advanced system settings".
The _System Properties_ dialog will appear. Next click the "Environment Variables" button.
Then click "New". Now enter __GPTKEY__ for _variable_ name and then your API Key for _value_.
Done.

![Windows System Properties](images/envvar.png "Environment Variables on Windows System")

#### For Linux (or Mac)
set your GPTKEY in your .profile file in your home directory:  

export GPTKEY="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"  

Don't forget to reboot.

### The second option is to edit the gptgui.ini file 

The gptgui.ini file is in the gptgui (application's) directory.  
With notepad (for Windows) or any plain text editor of your choice, 
open the file and on the third line type:

gptkey=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

using you own key. It's the same procedure on any Linux or Mac system.  

So you have two options to set up the account KEY from Gpt.

---

## A few more notes

---

### gptgui.ini file

__gptgui.ini__ is a plain text file.
Three things can be set in the gptgui.ini file
- Theme
- Path and filename for the query-save file
- Your GPTKEY value (required - if not using system Environment Variable)

Possible themes are: __solar, superhero, cyborg, and darkly__.

You should enter a path with a file name that will be the  
plain text file where you can "Save" individual query responses.  
Call it anything you like.

example:  
>path=c:\gptgui\myqueries.txt  
theme=cyborg  
gptkey=your.own.gptkey.from.your.own.openai.account...  

_Note: if you've set up the GPTKEY in your system ENV,  
then do not enter anything on the third line of gptgui.ini._

---

![alttext](images/GptGUI.png "GptGUI simple interface")

__Input your query in the top box; hit Enter or click "Query".__  
The Gpt AI response will appear just below.  

The buttons:
- Clear
> Clears the query box and the response area.
- Save
> Save the response area with the query into your myqueries.txt file
that was set up in gptgui.ini.
- View
> Displays the myqueries.txt file you set up in gptgui.ini.  
You cannot edit the file hear.
- Purge
> Clears the contens of the myqueries.txt file.

---
