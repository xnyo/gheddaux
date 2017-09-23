## nazibot
### A Discord bot that acts like a nazi
This bot basically deletes messages that contain banned words. That's it.

### Requirements
- Python 3.4+
- SQLite 3 ODBC Driver
- A Discord Bot

### Setting up
```
$ git clone ...
$ cd nazibot
$ virtualenv -p $(which python3) .pyenv
$ source .pyenv/bin/activate
(.pyenv)$ pip install -r requirements.txt
(.pyenv)$ cp settings.sample.ini settings.ini
(.pyenv)$ nano settings.ini
...
(.pyenv)$ python3 nazibot.py
```
_(you can use tmux/screen/nohup/etc to run the bot)_

### Commands
- `;censor <word>` - Adds a word to banned word's list
- `;uncensor <word>` - Removes a word from banned word's list
- `;censoredwords` - List all censored words
_These commands can be used only by users who have the **General Permissions/Administration** permission._
_**Messages from administrator users won't be censored.**_

### LICENSE
MIT