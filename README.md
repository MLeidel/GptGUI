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
an API Key__.  
There is no cost to do so.

### Your Gpt API key will look someting like this:
>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

After starting the app the first time hit __Control-k__ on your
keyboard.
Then copy and past your API key into the box and click "OK".

![input box](images/gptguiKey.png "input gpt key")

---

## A few more notes

---

### gptgui.ini file

__gptgui.ini__ is a plain text file.
Two things can be set in the gptgui.ini file
- Theme
- Path and filename for the query-save file

Possible themes are: __solar, superhero, cyborg, and darkly__.

You should enter a path with a file name that will be the
plain text file where you can "Save" individual query responses.
Call it anything you like.

example:
>path=c:\\gptgui\\_myqueries.txt_  
theme=cyborg

---

![alttext](images/GptGUI.png "GptGUI simple interface")

__Input your query in the top box; hit Enter or click "Query".__  
The Gpt AI response will appear just below.

The buttons:
- Clear
> Clears the query box and the response area.
- Save
> Save the response area with the query into your _myqueries.txt_ file
that was set up in gptgui.ini.
- View
> Displays the _myqueries.txt_ file you set up in gptgui.ini.
You cannot edit the file hear.
- Purge
> Clears the contens of the _myqueries.txt_ file.

---
