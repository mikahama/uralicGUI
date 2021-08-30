#!/bin/bash

python3 setup.py bdist_mac
cp -R /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kivy/* ./build/uralicNLP.app/Contents/MacOS/lib/kivy/
codesign --remove-signature ./build/uralicNLP.app/Contents/MacOS/lib/Python
cp rootroo.png ./build/uralicNLP.app/Contents/MacOS/rootroo.png
cp -r build/uralicNLP.app mac_dist_files/

#put platypus stuff there (this will setup the environment variables so that utf-8 works and CG3 can be accessed)
mv mac_dist_files/uralicNLP.app/Contents/MacOS/run mac_dist_files/uralicNLP.app/Contents/MacOS/run2
cp mac_auxiliary_files/Launcher.app/Contents/MacOS/Launcher mac_dist_files/uralicNLP.app/Contents/MacOS/run
cp -r mac_auxiliary_files/Launcher.app/Contents/Resources/* mac_dist_files/uralicNLP.app/Contents/Resources/

#remove stuff that prevents notarization. Zzzz...
rm -rf mac_dist_files/uralicNLP.app/Contents/MacOS/lib/joblib/test/data/
rm -rf mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/tests/unicode_files.zip

#unsign the signed grabage
#cp -f /Library/Frameworks/Python.framework/Versions/3.8/lib/libssl.1.1.dylib mac_dist_files/uralicNLP.app/Contents/MacOS/libssl.1.1.dylib
#cp -f /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/lib-dynload/_hashlib.cpython-38-darwin.so mac_dist_files/uralicNLP.app/Contents/MacOS/lib/_hashlib.cpython-38-darwin.so
#cp -f /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/lib-dynload/_ssl.cpython-38-darwin.so mac_dist_files/uralicNLP.app/Contents/MacOS/lib/_ssl.cpython-38-darwin.so
#codesign --remove-signature mac_dist_files/uralicNLP.app/Contents/MacOS/lib/readline.cpython-38-darwin.so #ok
#cp -f /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kivy/.dylibs/SDL2 mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/.dylibs/SDL2
#cp -f /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kivy/.dylibs/SDL2_image mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/.dylibs/SDL2_image
#cp -f /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kivy/.dylibs/webp mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/.dylibs/webp

mv  mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/.dylibs/ mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/dylibs/
mv mac_dist_files/uralicNLP.app/Contents/MacOS/lib/numpy/.dylibs mac_dist_files/uralicNLP.app/Contents/MacOS/lib/numpy/dylibs
mv mac_dist_files/uralicNLP.app/Contents/MacOS/lib/sklearn/.dylibs mac_dist_files/uralicNLP.app/Contents/MacOS/lib/sklearn/dylibs
mv mac_dist_files/uralicNLP.app/Contents/MacOS/lib/scipy/.dylibs mac_dist_files/uralicNLP.app/Contents/MacOS/lib/scipy/dylibs
#codesign --force -s "Developer ID Application: Rootroo Oy (Y9AT28Z65S)" --timestamp -o runtime mac_dist_files/uralicNLP.app/Contents/MacOS/run
#codesign -s "Developer ID Application: Rootroo Oy (Y9AT28Z65S)" --timestamp -o runtime mac_dist_files/uralicNLP.app/Contents/MacOS/run2
codesign --force -s "Developer ID Application: Rootroo Oy (Y9AT28Z65S)" --timestamp -o runtime --deep mac_dist_files/uralicNLP.app

mv  mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/dylibs/ mac_dist_files/uralicNLP.app/Contents/MacOS/lib/kivy/.dylibs/
mv mac_dist_files/uralicNLP.app/Contents/MacOS/lib/numpy/dylibs mac_dist_files/uralicNLP.app/Contents/MacOS/lib/numpy/.dylibs
mv mac_dist_files/uralicNLP.app/Contents/MacOS/lib/sklearn/dylibs mac_dist_files/uralicNLP.app/Contents/MacOS/lib/sklearn/.dylibs
mv mac_dist_files/uralicNLP.app/Contents/MacOS/lib/scipy/dylibs mac_dist_files/uralicNLP.app/Contents/MacOS/lib/scipy/.dylibs

#make a dmg
rm -f mac_dist_files/uralicNLP.dmg
appdmg mac_auxiliary_files/dmg.json mac_dist_files/uralicNLP.dmg
