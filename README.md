# QuickFolder
A little Python script to bind keypresses and/or key combinations to open a folder,
or execute a command.

# Motivations
I've created this script mainly for the purposes of efficiency. I'm very obsessed with
reducing the use of my mouse. This tool allows me to quickly open up common folders I
use, very quickly.

# Setup
This script requires the Keyboard module to function correctly, so unless you're using
a compiled binary, you have to install this through Pip. You'll also want to setup the
file manager that you'll be using. It has to be invokable through the command line, and
accept a directory to open as an argument for it to be usable. To do this, simply change
the file manager key in SETUP to the command to invoke the file manager through a CLI.

This script automatically adds itself to the Startup registry, but only on Windows
devices. You'll have to do this manually on Linux Linux, and Mac.

Now to actually create key combinations, add a new key in keybindings.ini. The format for
keyboard shortcuts is: key+key. Each key must be separated by a + sign, and once you're
done writing your key combination, put an equals sign then the path to the folder, like
so:

```
ctrl+shift+e = C:\Windows
```

To execute a command, simply replace the directory with the command you want to execute.
Simple as that. here's an example that opens notepad when you press ctrl+shift+e:

```
ctrl+shift+e = notepad
```

You can also do additional configuration like changing the periods between re-binding keys
to check for new keys being added, and the file manager that the script uses.

# Notice(s)
I've realized that Windows Defender seems to accuse the .EXE of being a virus. This is
a false positive that I believe to be caused by the script using the Keyboard module.
The Keyboard module makes no attempt to hide itself (as stated on the PyPi page.)
Because of this, you'll have to add this to an exclusion file for Windows Defender, or
whatever other antivirus you use.

Each keypress is hooked *globally*. This means that they will be detected regardless
of the program being in focus.