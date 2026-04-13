import sys
import os
import subprocess
from pathlib import Path

def find_or_create_venv():
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    return venv_path

def install_dependencies(venv_path):
    pip_path = venv_path / "Scripts" / "pip" if os.name == 'nt' else venv_path / "bin" / "pip"
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "rich", "google-genai", "python-dotenv"], check=True)

def setup_config(target_dir):
    print("\n--- AI Reviewer Configuration ---")
    api_key = input("Enter your Gemini API Key: ").strip()
    while not api_key:
        api_key = input("API Key is required: ").strip()
    
    model = input("Model (default: gemini-1.5-flash): ").strip() or "gemini-1.5-flash"
    lang = input("Language (default: English): ").strip() or "English"

    env_path = target_dir / ".git-reviewer" / ".env"
    with open(env_path, "w") as f:
        f.write(f"API_KEY={api_key}\nAI_MODEL={model}\nREVIEW_LANGUAGE={lang}\n")
    
    exclude_path = target_dir / ".git" / "info" / "exclude"
    if exclude_path.exists():
        content = exclude_path.read_text()
        if ".git-reviewer/" not in content:
            with open(exclude_path, "a") as f:
                f.write("\n.git-reviewer/\n")

def main():
    current_dir = Path.cwd()
    is_subfolder = current_dir.name == ".git-reviewer"
    target_dir = current_dir.parent if is_subfolder else current_dir

    venv_path = find_or_create_venv()
    install_dependencies(venv_path)
    setup_config(target_dir)

    hooks_path = target_dir / ".git" / "hooks"
    hook_file = hooks_path / "pre-commit"

    rel_path = ".git-reviewer/" if is_subfolder else ""
    python_bin = f"$REPO_ROOT/{rel_path}.venv/bin/python"
    main_script = f"$REPO_ROOT/{rel_path}main.py"

    bash_template = f"""#!/bin/bash
REPO_ROOT=$(git rev-parse --show-toplevel)
PYTHON_BIN="{python_bin}"
MAIN_SCRIPT="{main_script}"
exec < /dev/tty
"$PYTHON_BIN" "$MAIN_SCRIPT"
exit $?
"""

    hook_file.write_text(bash_template, encoding="utf-8")
    hook_file.chmod(0o755)
    print("Git Hook installed successfully.")

if __name__ == "__main__":
    main()