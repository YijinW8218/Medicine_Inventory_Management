# Medicine Inventory Management System

## Introduction

Medicine Inventory Management System is a desktop application for maintaining a hospital medicine inventory. Built with Python, Tkinter, and Excel-backed storage, it supports medicine and batch creation, removal, search, inventory reporting, and dispensing medicine by earliest-expiry priority.

## Environment Requirements

- Python 3.10 to 3.13
- Tkinter, included with most standard Python installations
- pandas 2.0 or later
- openpyxl 3.1 or later

The application stores its data in `store.xlsx`. Keep that file in the same folder as the Python source files. A backup workbook is provided as `store_copy.xlsx`.

## Installation

1. Clone or download this repository.
2. Open a terminal in the downloaded project folder.
3. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install the required packages:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Usage

Start the application with:

```bash
python3 main.py
```

At the welcome screen, enter the included demonstration password: `123456`.

Use the menu to create medicines, add batches, remove records, dispense available medicine, search the inventory, or generate reports. Changes are saved to `store.xlsx` when the menu window is closed.

## Project Structure

- `main.py` starts the application.
- `gui.py` provides the Tkinter user interface.
- `file_manager.py` reads and writes the Excel inventory workbook.
- `formulas.py` contains the inventory models and priority logic.
- `formulas_test.py` contains unit tests for the inventory logic.
- `store.xlsx` is the active inventory data file.
- `store_copy.xlsx` is a backup copy of the inventory data.
