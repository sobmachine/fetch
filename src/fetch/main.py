import sys
import os
from PIL import Image
from colorama import Style, init
import platform
import psutil
import datetime
import random
import subprocess

init(autoreset=True)

# === ASCII setup ===
ASCII_CHARS = "▒▒▒▒▒▒▒▒▒ "

def resize_image(image, new_width=50):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.50)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    return "".join([ASCII_CHARS[pixel * (len(ASCII_CHARS)-1) // 255] for pixel in pixels])

def colorize_ascii(image, ascii_str):
    colored_str = ""
    pixels = list(image.convert("RGB").getdata())
    width = image.width
    for i, char in enumerate(ascii_str):
        r, g, b = pixels[i]
        colored_str += f"\033[38;2;{r};{g};{b}m{char}{Style.RESET_ALL}"
        if (i + 1) % width == 0:
            colored_str += "\n"
    return colored_str

def image_to_ascii(image_path, new_width=50):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    image = Image.open(image_path)
    image = resize_image(image, new_width)
    image_gray = grayify(image)
    ascii_str = pixels_to_ascii(image_gray)
    return colorize_ascii(image, ascii_str), image

# === Pick readable color from image ===
def pick_color_from_image(image):
    pixels = list(image.convert("RGB").getdata())
    while True:
        r, g, b = random.choice(pixels)
        brightness = (r*0.299 + g*0.587 + b*0.114)
        if 50 < brightness < 200:
            return r, g, b

# === CPU name for Termux/Linux ===
def get_cpu_name():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.strip().startswith("Hardware"):
                    return line.strip().split(":")[1].strip()
                elif line.strip().startswith("model name"):
                    return line.strip().split(":")[1].strip()
    except Exception:
        pass
    return platform.processor() or "Unknown CPU"

# === OS info with Android/Linux detection ===
def get_os_info():
    # Android detection
    if "android" in platform.system().lower() or os.path.exists("/system/build.prop"):
        try:
            release = subprocess.check_output(["getprop", "ro.build.version.release"], text=True).strip()
        except Exception:
            release = "Unknown"
        try:
            brand = subprocess.check_output(["getprop", "ro.product.brand"], text=True).strip()
        except Exception:
            brand = "Android"
        try:
            model = subprocess.check_output(["getprop", "ro.product.model"], text=True).strip()
        except Exception:
            model = ""
        return f"{brand} {model} Android {release}".strip()
    
    # Linux fallback
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                data = f.read()
            name_line = next((l for l in data.splitlines() if l.startswith("PRETTY_NAME=")), None)
            if name_line:
                return name_line.split("=")[1].strip('"')
    except Exception:
        pass
    
    return platform.system()

# === Kernel version ===
def get_kernel_version():
    try:
        return platform.release()
    except Exception:
        return "Unknown"

# === System info colored from image ===
def get_colored_system_info(image):
    ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
    cpu_count = psutil.cpu_count(logical=True)

    # Termux-friendly uptime
    try:
        with open("/proc/uptime") as f:
            uptime_seconds = float(f.readline().split()[0])
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    except Exception:
        uptime_str = "Unknown"

    # Disk usage
    try:
        disk = psutil.disk_usage("/")
        disk_total = round(disk.total / (1024**3), 2)
        disk_used = round(disk.used / (1024**3), 2)
    except Exception:
        disk_total, disk_used = 0, 0

    info_text = [
        f"OS: {get_os_info()}",
        f"Kernel: {get_kernel_version()}",
        f"Machine: {platform.machine()}",
        f"Processor: {get_cpu_name()}",
        f"CPU Cores: {cpu_count}",
        f"RAM: {ram_gb} GB",
        f"Disk: {disk_used}/{disk_total} GB",
        f"Uptime: {uptime_str}",
        f"Python: {platform.python_version()}"
    ]

    # Color each line from the image
    colored_lines = []
    for line in info_text:
        r, g, b = pick_color_from_image(image)
        colored_lines.append(f"\033[38;2;{r};{g};{b}m{line}{Style.RESET_ALL}")

    return colored_lines

# === Merge ASCII + system info ===
def print_ascii_with_info(ascii_art, info_lines):
    ascii_lines = ascii_art.split("\n")
    max_lines = max(len(ascii_lines), len(info_lines))
    ascii_width = max(len(line) for line in ascii_lines)

    for i in range(max_lines):
        art_line = ascii_lines[i] if i < len(ascii_lines) else " " * ascii_width
        info_line = info_lines[i] if i < len(info_lines) else ""
        print(f"{art_line}   {info_line}")

# === CLI ===
def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = sys.stdin.readline().strip()

    if not os.path.exists(path):
        print("❌ 0x001F - File not found")
        sys.exit(1)

    ascii_art, img_for_colors = image_to_ascii(path, new_width=50)
    info = get_colored_system_info(img_for_colors)
    print_ascii_with_info(ascii_art, info)

if __name__ == "__main__":
    main()
