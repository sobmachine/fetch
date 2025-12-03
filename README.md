# Fetch

![Stars](https://img.shields.io/github/stars/sobmachine/fetch?style=flat&color=C9A7FF&logo=github)
![License](https://img.shields.io/github/license/sobmachine/fetch?style=flat&color=BF8BFF&logo=gnu)
![Python](https://img.shields.io/badge/Python-3.12-BA9CFF?style=flat&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-lavender?logo=windows-10&logoColor=white&color=B57EDC)
![Linux](https://img.shields.io/badge/Linux-lavender?logo=linux&logoColor=black&color=B57EDC)
![macOS](https://img.shields.io/badge/macOS-lavender?logo=apple&logoColor=white&color=B57EDC) 

*Fetch* is a *lightweight, terminal-based system info and image ASCII art display tool*, inspired by Neofetch. It converts any image into colored ASCII art while showing detailed system information in a visually appealing way.

This project is designed to run on Linux, Android (Termux), and other Unix-like environments.

---

## Features

- Image-to-ASCII Conversion: 
Converts your wallpapers or images into colorful ASCII art in the terminal, preserving approximate colors from the original image.
- System Information
Displays key system details like: 
   - Operating System & Version
   - Kernel Version
   - Device Model / Machine Architecture
   - Processor and CPU Cores
   - RAM Usage
   - Disk Usage
   - Uptime (if available)
   - Python Version
- Dynamic Coloring: 
Each ASCII character’s color is derived from the original image, ensuring a vibrant, faithful representation.
- CLI Friendly: 
Works directly from the terminal. Simply provide an image path as an argument, or pipe in a path via stdin.

---

## Installation

Using Git
```bash
git clone https://github.com/sobmachine/fetch.git
cd fetch
pip install .
```

This will install "fetch" as a CLI tool accessible from anywhere.

---

## Dependencies

- Python 3.8+
- [Pillow](https://pillow.readthedocs.io/) – for image processing
- [Colorama](https://pypi.org/project/colorama/) – for terminal coloring
- [psutil](https://pypi.org/project/psutil/) – for system information

All dependencies are included in "requirements.txt" and installed automatically via "pip".

---

## Usage

```bash
# Basic usage with an image path
fetch path/to/image.png


# Example
fetch ~/Downloads/wallpaper.jpg
```

If no path is provided, "fetch" will read the path from standard input:

```bash
echo ~/Downloads/wallpaper.jpg | fetch
```

---

Output Example

![Alt text](assets/run.png)

---

Development & Contribution

- Source Code: Located in "src/fetch/main.py".
- Packaging: Uses "pyproject.toml" for pip installation.
- Standalone Executable: Can be compiled with "Nuitka" (https://nuitka.net/) for fully self-contained binaries.

Contributions are welcome! Feel free to submit pull requests or open issues with feature requests or bug reports.

---

License

Fetch is released under the GNU GPL v3. You are free to modify and distribute the software, but derivative works must also be licensed under the GPL.
