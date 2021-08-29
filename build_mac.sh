#!/bin/bash

#python3 setup.py py2app
#python3 -m PyInstaller --exclude-module enchant --exclude-module twisted --exclude-module _tkinter --exclude-module Tkinter --clean --windowed --name uralicNLP run.py

python3 setup.py bdist_mac
cp -R /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kivy/* ./build/uralicNLP.app/Contents/MacOS/lib/kivy/
codesign --remove-signature ./build/uralicNLP.app/Contents/MacOS/lib/Python
cp rootroo.png ./build/uralicNLP.app/Contents/MacOS/rootroo.png
cp -r build/uralicNLP.app mac_dist_files/
#ln -s /usr/local/bin/vislcg3 mac_dist_files/uralicNLP.app/Contents/MacOS/vislcg3
#ln -s /usr/local/bin/cg-conv mac_dist_files/uralicNLP.app/Contents/MacOS/cg-conv
mv mac_dist_files/uralicNLP.app/Contents/MacOS/run mac_dist_files/uralicNLP.app/Contents/MacOS/run2
cp mac_auxiliary_files/Launcher.app/Contents/MacOS/Launcher mac_dist_files/uralicNLP.app/Contents/MacOS/run
cp -r mac_auxiliary_files/Launcher.app/Contents/Resources/* mac_dist_files/uralicNLP.app/Contents/Resources/
rm -f mac_dist_files/uralicNLP.dmg
appdmg mac_auxiliary_files/dmg.json mac_dist_files/uralicNLP.dmg