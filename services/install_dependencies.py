import os
import subprocess



from services.theme import console


def install_dependencies(venv_path):
    pip_path = venv_path / "Scripts" / "pip" if os.name == 'nt' else venv_path / "bin" / "pip"
    console.print("[info]Installing dependencies (rich, google-genai, python-dotenv)...[/info]")
    subprocess.run([str(pip_path), "install", "rich", "google-genai", "python-dotenv"], stdout=subprocess.DEVNULL)