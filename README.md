# GptGUI

Python GUI for Linux or Windows to access OpenAI Gpt Engine.

Before using this application Python 3.x must be installed.

To install Python go to https://www.python.org/downloads/.
Click __Download Python 3.???__ and follow the installation instructions.

You will also have to Sign Up at https://openai.com/api/ and __create
anAPI Key__.  
There is no cost to do so.

There are two ways to apply the key to the program.  
### The first way is to set the GPTKEY as an environment variable.  
#### For Windows it goes like this:  
Finally, you will have to edit the Windows _system environment variables_ to add
the API Key. To do this go to the start menu and begin typing "advanced system settings".
The System Properties dialog will appear. Next click the "Environment Variables" button.
Then click "New". Hear enter __GPTKEY__ for _variable_ name and then your API Key for _value_.
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

Except use your own key. It's the same procedure on any system.  

So its option 1 or 2 whatever you prefer.

---

## Now install GptGUI.

---

If you're able to get it installed here are a few things to note.

## gptgui.ini file

__gptgui.ini__ is a plain text file.
Three things can be set in the gptgui.ini file
- Theme
- Path and filename for the query-save file
- Your GPTKEY value (required if not using system Env Variable)

example:
__theme=superhero__  
Possible themes are: solar, superhero, cyborg, and darkly.

The query-save file is also a plain text file where you can save (append) individual
queries.

example:  
>__path=c:\gptgui\myqueries.txt__  
__theme=cyborg__  
__gptkey=__your.own.gptkey.from.openai...  

_Note: if you've set up the GPTKEY in your system ENV,  
then do not enter anything on the third line of gptgui.ini._

---

![alttext](images/GptGUI.png "GptGUI simple interface")

__Input your query in the top box; hit Enter or click "Query".__  
Gpt response will appear just below.  

The buttons:
- Clear
> Clears the query box and the response area.
- Save
> Save the response area with the query into your querysave file
that was set up in gptgui.ini.
- View
> Brings up the querysave file in the response area for viewing.  
No editing.
- Purge
> Clears the contens of the querysave file.







