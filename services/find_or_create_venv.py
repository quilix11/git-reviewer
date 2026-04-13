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
                print(f"[info]Found non-standard virtual environment: {d.name}[/info]")
                return d
                
    print("[info]Virtual environment not found. Creating .venv...[/info]")
    subprocess.run([sys.executable, "-m", "venv", ".venv"])
    return root / ".venv"