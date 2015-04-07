# ORGANIZE Register Application


## If you get an error when running ```./manage.py compilemessages``` or ```./manage.py makemessages```

Error: 

```
CommandError: Can't find msgfmt. Make sure you have GNU gettext tools 0.15 or newer installed.
```

Run:

```
brew install gettext
brew link gettext --force
```
