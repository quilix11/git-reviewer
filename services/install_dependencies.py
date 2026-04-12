import os
import subprocess



def install_dependencies(venv_path):
    pip_path = venv_path / "Scripts" / "pip" if os.name == 'nt' else venv_path / "bin" / "pip"
    print("⏳ Встановлюю залежності (rich, google-genai, python-dotenv)...")
    subprocess.run([str(pip_path), "install", "rich", "google-genai", "python-dotenv"], stdout=subprocess.DEVNULL)