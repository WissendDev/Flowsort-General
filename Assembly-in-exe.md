pyinstaller --onefile --noconsole --icon="icon.ico" flowsort_core.py
pyinstaller --onefile --noconsole --uac-admin --icon="icon.ico" installer.py
pyinstaller --onefile --noconsole --uac-admin --icon="icon.ico" uninstaller.py