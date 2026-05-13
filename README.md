# QR Code Generator

QR Code Generator is a Python application for creating QR codes from text or links.
The project contains both a command-line interface and a graphical interface built with `tkinter`.

## Project Goal

The goal of the project is to demonstrate a complete small Python application with:

- QR code generation;
- PNG file saving;
- a desktop GUI;
- generation history;
- configurable QR style options;
- automated tests;
- clear Git history with feature commits, a separate branch, and a merge commit.

## Features

- generate QR codes from the command line;
- generate QR codes from a graphical interface;
- save generated QR codes as PNG files;
- choose the output folder and filename;
- customize QR box size and border;
- customize foreground and background colors;
- preview the generated QR code in the GUI;
- store the latest generated QR codes in `output/history.json`;
- open the output folder from the GUI;
- validate empty input and invalid style options.

## Project Structure

```text
KPZ/
├── qr_app/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── generator.py
│   ├── gui.py
│   └── history.py
├── tests/
│   ├── test_generator.py
│   └── test_history.py
├── .gitignore
├── README.md
└── requirements.txt
```

Main files:

- `qr_app/generator.py` contains QR generation and option validation logic.
- `qr_app/cli.py` contains the command-line interface.
- `qr_app/gui.py` contains the desktop graphical interface.
- `qr_app/history.py` stores and loads recent generated QR codes.
- `tests/` contains automated tests for the main logic.

## Requirements

- Windows 10/11 or another OS with Python support;
- Python 3.10 or newer;
- `pip`;
- Git.

If the `python` command opens Microsoft Store on Windows, install Python from:

```text
https://www.python.org/downloads/
```

During installation, enable:

```text
Add python.exe to PATH
```

## Installation

Open PowerShell in the project folder:

```powershell
cd E:\University\Task\KPZ
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

The project uses:

- `qrcode[pil]` for QR generation and PNG image saving;
- `pytest` for automated testing.

## Running The GUI

Start the graphical application:

```powershell
python -m qr_app --gui
```

In the GUI:

1. Enter text or a URL.
2. Choose the output PNG file.
3. Change QR style options if needed.
4. Click `Generate`.
5. Check the preview and recent QR history.
6. Use `Open folder` to open the folder with generated files.

## Running From Command Line

Generate a QR code with the default output path:

```powershell
python -m qr_app "https://example.com"
```

Save with a custom filename:

```powershell
python -m qr_app "Hello KPZ" --output output/hello.png
```

Use custom size, border, and colors:

```powershell
python -m qr_app "https://example.com" --output output/site.png --box-size 12 --border 5 --fill "#111111" --back "#ffffff"
```

Generated files are saved as PNG images. The default output folder is `output/`.

## Running Tests

Run all tests:

```powershell
python -m pytest
```

Expected result:

```text
9 passed
```

The tests check:

- PNG generation;
- empty input validation;
- invalid QR option validation;
- QR image creation;
- history saving and loading;
- broken history file handling.

## Git Workflow

This project demonstrates Git usage through:

- the `main` branch with the initial commit;
- the `qr-generator` feature branch with the main application;
- the `qr-history` feature branch for history-related functionality;
- a merge commit from `qr-history` into `qr-generator`;
- separated commits for each meaningful development step.

Useful commands for demonstration:

```powershell
git log --oneline --decorate --graph --all
git status
git branch
```

Current development history contains commits for:

1. initial QR generator;
2. basic GUI window;
3. connecting GUI to QR generation;
4. GUI controls and documentation;
5. consistent style option validation;
6. QR preview in GUI;
7. history storage;
8. history display in GUI;
9. output folder shortcut;
10. merge of the history feature.

## Notes

The `output/` folder is ignored by Git. It is created automatically when the application saves QR codes.

The history file is stored at:

```text
output/history.json
```
