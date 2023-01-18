# GptGUI

Python GUI for Linux or Windows to access OpenAI Gpt Engine.

Before using this application Python 3.x must be installed.

To install Python go to https://www.python.org/downloads/.  
Click __Download Python 3.???__ and follow the installation instructions.

You will also have to Sign Up at https://openai.com/api/ and __create
anAPI Key__. There is no cost to do so.

Finally, you will have to edit the Windows _system environment variables_ to add
the API Key. To do this go to the start menu and begin typing "_environmen_..." and _edit environment
variables_ will appear. Click it, and then click "environment variables", system "New".
Then enter __GPTKEY__ for _variable_ name and then your API Key for _value_.

Now install GptGUI.

Good Luck, and good night!

---

If you're able to get it installed here are a few things to note.

## gptgui.ini file

__gptgui.ini__ is a plain text file.
Three things can be set in the gptgui.ini file
- Theme
- Path and filename for the query-save file
- Your GPTKEY value (coming soon)

example:  
__theme=superhero__

Possible themes are: solar, superhero, cyborg, and darkly.

The query-save file is also a plain text file where you can save individual
queries when using this application.  

example:  
__path=c:\gptgui\myqueries.txt__  
__theme=cosmo__  
__gptkey=...........__

