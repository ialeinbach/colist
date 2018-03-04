# Colist
A plugin for Sublime Text 3 that formats multi-line lists into columns.
THIS IS VERY MUCH A WORK IN PROGRESS.

#### Usage Notes
Right now, the number of columns per line to format is a hard-coded value. Using a value larger tha$

#### Files In This Repo
`colist.py` contains the code for the plugin.   
`test.txt` contains a test file that exists in the scope of the current functionality of the plugin$

#### How To Try It Out
First, add `colist.py` to you packages folder. This varies based on your OS.

* **Windows:** %APPDATA%\Sublime Text 3
* **OS X:** /Users/{user}/Library/Application Support/Sublime Text 3/Packages
* **Linux:** ~/.config/sublime-text-3/Packages/

Open `test.txt` in Sublime 3 and select the whole file (`ctrl+a`). Open the console (``` ctrl+` ```) and run `view.run_command('colist')`.

#### TODO
* handle whitespace (i.e. be mindful of whitespace already present in list)
* handle varying columns per line (i.e. align as many columns as possible, then just space properly)
* handle nested commas (i.e. correctly formatting a list of lists/tuples/etc.)
* handle indentation of list (i.e. indent subsequent lines flush to first)
* handle list delimiters (i.e. ignore if selected? make design decision to require selecting inside$
