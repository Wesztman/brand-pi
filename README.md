# About The Project

Raspberry Pi code repository for the fire extinguisher robot of Team Bränd.

<!-- # Built With -->

# Getting Started

## Prerequisites

- Git - [Download & Install Git](https://git-scm.com/)
- VS Code - [Download & Install VS Code](https://code.visualstudio.com/)
- Python 3 - [Download & Install Python 3](https://www.python.org/downloads/)
> **_NOTE:_** Don´t forget to add python to PATH when installing Python 3.
____
## Installation
0. Clone the repository.
```bash
git clone https://github.com/Wesztman/brand-pi.git
```
1. Open VS Code and install the suggested extensions.

2. Create a virtual env where all dependencies/packages for this project will be installed.
```bash
python3 -m venv venv
```
activate the virtual environment by running `source venv/bin/activate`

3. Install required dependencies.
```bash
pip3 install -r requirements.txt
```

# Usage

## Logging
- Please use `logging.{level}("text")` instead of `print()` ex. `logging.warning("Unhandled robot state")`. Log files are saved in `logs/` and all logged lines will also be printed to console. Available log levels in falling severity are:
   - critical
   - error
   - warning
   - info
   - debug
   - notset

Current visible log level is set at logger initialization at top of main.
# License
Distributed under the MIT License. See `LICENSE` for more information.
<!-- # Contact -->

<!-- # Acknowledgements -->
