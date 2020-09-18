#!/usr/bin/python

import sys
import time
import winreg
import keyboard
from os import system
from configparser import ConfigParser
from argparse import ArgumentParser
from pathlib import Path

rootDir = list(Path(__file__).absolute().parents)[-3]  # -3 because it always ends up being the Project directory.
settingsFile = rootDir / Path("keybindings.ini")
exePath = rootDir / Path("bin/QuickFolder.exe")
keybindsParser = ConfigParser()
keybinds = []
isExe = False

keybindsParser.read(settingsFile)

# Dynamically remove and add the Exe to the startup registry if the running OS is Windows.
if sys.platform == "win32":
    # Get the key HKEY_CURRENT_USER so we can access the Startup registry with privileges
    # that allow us do anything to this key.
    accessKey = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    startupDir = winreg.OpenKey(accessKey, str(Path("Software/Microsoft/Windows/CurrentVersion/Run")),
                                0, winreg.KEY_ALL_ACCESS)

    # Dynamically sets or deletes the value in the Startup registry, based off
    # whether or not the Exe exists.
    if exePath.exists():
        winreg.SetValueEx(startupDir, "QuickFolder", 1, winreg.REG_SZ, str(exePath))
    else:
        try:
            # Remove the key assigned to QuickFolder, assuming it exists.
            winreg.DeleteValue(startupDir, "QuickFolder")
        except FileNotFoundError:
            pass

# Setup CLI arguments.
parser = ArgumentParser(description="Small CLI program to open folders from keystrokes.")
parser.add_argument("--validate", help="""Validates that all paths from keybinds.ini
                    exist. Does not work on commands.""", action="store_true")
parser.add_argument("--trim", help="Trims any paths that don't exist.", action="store_true")
CLIArgs = parser.parse_args()

# Trim any bad paths if requested.
if CLIArgs.trim:
    keybinds = keybindsParser["KEYBINDS"]
    keybindsParser["KEYBINDS"] = {short: location for short, location in keybinds.items() if Path(location).exists()}

    with open(settingsFile, "r") as settings:
        keybindsParser.write(settings)

# Yield indefinitely, until the user kills the program, while re-reading
# the keybindings file for new bindings.
try:
    while True:
        keybindsParser.read(settingsFile)
        fileManager = keybindsParser["SETUP"]["filemanager"]

        # Maps keybindings to directories, or commands
        for shortcut, directory in keybindsParser["KEYBINDS"].items():
            try:
                pathToDir = Path(directory)

                if pathToDir.exists() and pathToDir.is_dir():
                    keybinds.append(keyboard.add_hotkey(shortcut, lambda: system(f"{fileManager} {directory}")))
                elif CLIArgs.validate:
                    print(f"Bad directory path {directory}")
            except OSError:
                # This executing assumes that it is a *command* and not a directory
                # that needs to be opened.
                keybinds.append(keyboard.add_hotkey(shortcut, system, args=(directory,)))
            except ValueError:
                pass

        time.sleep(float(keybindsParser["SETUP"]["rebindWaitTime"]))

        # Destroy all keybinds, so we dont end up with multiple bindings.
        for keybinding in keybinds:
            keyboard.remove_hotkey(keybinding)
            del keybinding

        keybinds = []
        keybindsParser.clear()

except KeyboardInterrupt:
    pass
