## Gheddaux
### Ripple's Discord Bot, Schiavo's younger sibling
This is the source code that powers `Le Gheddaux de la Petrine`, one of
the bots we have on Ripple's discord server

### Features
- Deletes forbidden words
- Manages cheater reports in the `#playerreporting` channel
- Welcomes new users who join the server
- Basic moderation commands

### Requirements
- Python 3.5+
- A Discord Bot

### Setting up
```
$ git clone ...
$ cd gheddaux
$ virtualenv -p $(which python3) .pyenv
$ source .pyenv/bin/activate
(.pyenv)$ pip install -r requirements.txt
(.pyenv)$ cp settings.sample.ini settings.ini
(.pyenv)$ nano settings.ini
...
(.pyenv)$ python3 gheddaux.py
```

### Commands
- `;censor word` - Adds a word to banned word's list
- `;uncensor word` - Removes a word from banned word's list
- `;censoredwords` - List all censored words
- `;prune x` - Deletes x messages
- `;pruneu @user x` - Deletes x messages sent by @user
  
_These commands can be used only by users who have the **General Permissions/Administration** permission._

### LICENSE
MIT