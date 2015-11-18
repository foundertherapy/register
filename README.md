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
