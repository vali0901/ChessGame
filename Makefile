SHELL := /bin/bash

VENV = .venv/bin/

SRC = \
	$(shell ls src/pieces/*py) \
	$(shell ls src/*py)

DEPENDENCIES = \
	python3 \
	python3-pip \
	python3-venv \
	python3-tk

echo-src:
	echo $(SRC)

init-setup:
	sudo apt install -y $(DEPENDENCIES)
	touch -a init-setup

.venv/bin/pip:
	python3 -m venv .venv

install-req: .venv/bin/pip requirements.txt
	.venv/bin/pip install -r requirements.txt
	touch -a install-req

build: init-setup install-req $(SRC)
	.venv/bin/pyinstaller -F --name ChessGame --clean --add-data='img:img' --hidden-import='PIL._tkinter_finder' src/main.py

run: init-setup install-req
	.venv/bin/python3 src/main.py

run-exec: build
	./dist/ChessGame

clean:
	rm -rf .venv/
	rm -rf dist/
	rm -rf build/
	rm -f ChessGame.spec
	rm -f init-setup
	rm -f install-req
	rm -rf src/__pycache__/
	rm -rf src/pieces/__pycache__/
