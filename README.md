### Building
* Clone repository
* pip install -r .\requirements.txt
#### For Windows
pyinstaller -F --name ChessGame.exe --clean --add-data="img;img" main.py
#### For Linux 
pyinstaller -F --name ChessGame --clean --add-data='img:img' --hidden-import='PIL._tkinter_finder' main.py

Executable will be created in dist/ directory.
