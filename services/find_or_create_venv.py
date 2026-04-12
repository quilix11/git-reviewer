import os
import sys
import subprocess
from pathlib import Path


def find_or_create_venv():
    root = Path.cwd()
    
    for name in [".venv", "venv", "env"]:
        if (root / name / "pyvenv.cfg").exists():
            return root / name

    for d in root.iterdir():
        if d.is_dir() and d.name not in [".git", "node_modules", ".idea", "__pycache__"]:
            if (d / "pyvenv.cfg").exists():
                print(f"ℹ Знайдено нестандартне віртуальне середовище: {d.name}")
                return d
                
    print("⏳ Віртуальне середовище не знайдено. Створюю .venv...")
    subprocess.run([sys.executable, "-m", "venv", ".venv"])
    return root / ".venv"