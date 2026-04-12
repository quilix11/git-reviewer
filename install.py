import sys
from pathlib import Path
from services.find_or_create_venv import find_or_create_venv
from services.install_dependencies import install_dependencies
from services.theme import console

venv_path = find_or_create_venv()

install_dependencies(venv_path)

hooks_path = Path(".git/hooks")
hook_file = hooks_path / "pre-commit"

if not hooks_path.exists():
    console.print("[error].git/hooks folder not found. Are you sure you're in the root of a Git project?[/error]")
    sys.exit(1)

try:
    user_lang = console.input("[prompt]Enter language for AI responses: [/prompt]").strip()
except EOFError:
    user_lang = "English"

if not user_lang:
    user_lang = "English"


bash_template = f"""#!/bin/bash
echo "Starting AI Git-Hook Reviewer..."

export REVIEW_LANGUAGE="{user_lang}"

REPO_ROOT=$(git rev-parse --show-toplevel)

PYTHON_BIN="$REPO_ROOT/{venv_path.name}/bin/python"
MAIN_SCRIPT="$REPO_ROOT/main.py"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Virtual environment {venv_path.name} not found in $REPO_ROOT"
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