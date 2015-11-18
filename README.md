# ORGANIZE Register Application

## How to Internationalize

1. Make sure you have ```gettext``` installed:

    ```
    brew install gettext
    ```

1. (Re)Generate the ```django.po``` file:

    ```
    ./manage.py makemessages -a
    ```

1. Update the ```django.po``` file to remove commented out translation strings from previous version of file. Be careful that the strings are all used.

1. Gather the strings that don't have translations (the ones that have ```msgstr ""``` and get translations for them.

1. Enter the translated strings into the correct records.

1. Compile the translation file (```django.mo```):

```
./manage.py compilemessages
```

1. Test the web app to make sure all strings that should be translated are showing up as translated. You may need to restart your local development server to pick up the changed ```django.mo``` file.


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
