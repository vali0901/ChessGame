
### Building

* Clone repository
* $ cd ChessGame/

#### Using Makefile (Linux)

make run - run using interpreter

make build - build executable

make run-exec - run build executable

#### Manual (Windows and Linux)

Prerequisites: python3, python3-pip python3-venv, python3-tk.

* $ python3 -m venv .venv
* Linux - $ source .venv/bin/activate
* Windows
  * cmd - $ .venv\Scripts\Activate.bat
  * Powershell - $ .\.venv\Scripts\Activate.ps1
* $ pip install -r ./requirements.txt
* Windows - $ pyinstaller -F --name ChessGame.exe --clean --add-data="img;img" ./src/main.py
* Linux  - $ pyinstaller -F --name ChessGame --clean --add-data='img:img' --hidden-import='PIL._tkinter_finder' ./src/main.py

Executable will be created in dist/ directory.
