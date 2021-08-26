#!/bin/bash

#python3 setup.py py2app
#python3 -m PyInstaller --exclude-module enchant --exclude-module twisted --exclude-module _tkinter --exclude-module Tkinter --clean --windowed --name uralicNLP run.py

python3 setup.py bdist_mac
cp -R /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kivy/* ./build/uralicNLP.app/Contents/MacOS/lib/kivy/
codesign --remove-signature /Users/mikahama/uralicGUI/build/uralicNLP.app/Contents/MacOS/lib/Python
cp rootroo.png ./build/uralicNLP.app/Contents/MacOS/rootroo.png