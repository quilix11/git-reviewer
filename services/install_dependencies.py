import os
import subprocess
import sys

from services.theme import console

def install_dependencies(venv_path):
    pip_path = venv_path / "Scripts" / "pip" if os.name == 'nt' else venv_path / "bin" / "pip"
    console.print("[info]Installing dependencies (rich, google-genai, python-dotenv)...[/info]")
    
    # Upgrade pip first
    result = subprocess.run(
        [str(pip_path), "install", "--upgrade", "pip"],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        console.print(f"[error]Failed to upgrade pip[/error]")
        sys.exit(1)
    
    # Install required packages
    result = subprocess.run(
        [str(pip_path), "install", "rich", "google-genai", "python-dotenv"],
        text=True,
        timeout=300
    )
    
    if result.returncode != 0:
        console.print(f"[error]Failed to install dependencies[/error]")
        sys.exit(1)
    
    console.print("[success]Dependencies installed successfully![/success]")
