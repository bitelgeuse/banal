import os

os.system("python -m venv venv")
if os.name == "nt":
    os.system(os.path.join("venv", "Scripts", "pip.exe") + " install -r requirements.txt")
else:
    os.system(os.path.join("venv", "bin", "pip") + " install -r requirements.txt")
