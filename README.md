# GptGUI
_Python GUI for Linux or Windows to access OpenAI Gpt Engine._

## Instalation

For windows you can downolad the setup_GptGUI.exe file supplied with this repo.

For Linux / Mac you can either _gh repo clone MLeidel/GptGUI_ or download a zip
file of this repo.


Before using this application Python 3.x must be installed.

To install Python go to https://www.python.org/downloads/.  
Click __Download Python 3.???__ and follow the installation instructions.


> ___
You will also have to Sign Up at https://openai.com/api/ and __create
an API Key__.  
There is no cost to do so.
___

### Your Gpt API key will look someting like this:
>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

After starting the app the first time click the _Options_
button.

Copy and past your API key into the "Gpt Key" entry box.  
A better way to handle your API key is to set it up in a System Environment Variable.  
Then put the variable's name into the "Gpt Key" entry box.

Change any other appearance or Gpt options as well.  
Then click the _Save & Close_ button.

![input box](images/gptopts.png "GptGUI options window")

---

## A few more notes

---

### gptgui.ini file

The options are stored in a plain text file called _gptopt.ini_.  
If you prefer you could change the settings with a text editor.

### Windows OS

There is a __setup\_GptGUI.exe__ included in the repository providing
a simple installation for Windows users.

---

### Using

![alttext](images/gptgui.png "Ctrl-t for Response Metrics")

Input your query in the top box, and hit __"Submit Query"__ or _Ctrl-g_.  
The Gpt AI response will appear in the larger box below.

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
- Options
> launches the Options editor.

---

## Hot Keys

![Tokens](images/gptkeys.png "Hot Keys")

----
END
