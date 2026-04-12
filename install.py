import sys
from pathlib import Path
from services.find_or_create_venv import find_or_create_venv
from services.install_dependencies import install_dependencies
from services.theme import console

venv_path = find_or_create_venv()

install_dependencies(venv_path)

current_dir = Path.cwd()
is_subfolder_install = current_dir.name == ".git-reviewer"
target_dir = current_dir.parent if is_subfolder_install else current_dir

hooks_path = target_dir / ".git" / "hooks"
hook_file = hooks_path / "pre-commit"

if not hooks_path.exists():
    console.print(f"[error].git/hooks folder not found in {target_dir}. Are you sure you're in a Git project?[/error]")
    sys.exit(1)

user_lang = sys.argv[1] if len(sys.argv) > 1 else "English"

rel_tool_path = ".git-reviewer/" if is_subfolder_install else ""

bash_template = f"""#!/bin/bash
echo "Starting AI Git-Hook Reviewer..."

export REVIEW_LANGUAGE="{user_lang}"

REPO_ROOT=$(git rev-parse --show-toplevel)

PYTHON_BIN="$REPO_ROOT/{rel_tool_path}{venv_path.name}/bin/python"
MAIN_SCRIPT="$REPO_ROOT/{rel_tool_path}main.py"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Virtual environment not found at $PYTHON_BIN"
    exit 1
fi

exec < /dev/tty

"$PYTHON_BIN" "$MAIN_SCRIPT"

RESULT=$?
exit $RESULT
"""

hook_file.write_text(bash_template, encoding="utf-8")
hook_file.chmod(0o755)
console.print("[success]Git Hook successfully installed in .git/hooks/pre-commit[/success]")