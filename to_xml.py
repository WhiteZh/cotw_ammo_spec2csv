import subprocess
from pathlib import Path, PosixPath

exe_name = r"C:\Users\johnb\Downloads\Ashen-Mod-Tools-for-JC4\AvalancheData.exe"
root_dir = Path(".")

valid_files = [file for file in root_dir.glob("**/*.ammotunec") if isinstance(file, Path)]

for file in valid_files:
    subprocess.run([exe_name, str(file.resolve())], input="\r\n", text=True, timeout=10, check=True)

