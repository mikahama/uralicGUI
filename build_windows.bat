rem pyinstaller run.py --noconfirm --icon uralic64.ico
pyinstaller run.spec --noconfirm --clean
mkdir dist\run\uralicNLP
mkdir dist\run\uralicGUI
copy /y lang_codes.json dist\run\uralicNLP\lang_codes.json
copy /y rootroo.png dist\run\rootroo.png

copy /y uralicGUI\uralic.kv dist\run\uralicGUI\uralic.kv
