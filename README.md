# QR Code Generator

Python application for generating QR codes from text or links.

## Features

- generate QR codes from the command line;
- save images as PNG files;
- choose output folder and filename;
- customize QR size, border, fill color, and background color;
- validate empty input before generation.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Generate a QR code:

```powershell
python -m qr_app "https://example.com"
```

Save with a custom filename:

```powershell
python -m qr_app "Hello KPZ" --output result.png
```

Use custom colors:

```powershell
python -m qr_app "https://example.com" --fill "#111111" --back "#ffffff"
```

Run tests:

```powershell
python -m pytest
```
