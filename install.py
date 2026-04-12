import sys
from pathlib import Path
from services.find_or_create_venv import find_or_create_venv
from services.install_dependencies import install_dependencies

venv_path = find_or_create_venv()

install_dependencies(venv_path)

hooks_path = Path(".git/hooks")
hook_file = hooks_path / "pre-commit"

if not hooks_path.exists():
    print("❌ Папку .git/hooks не знайдено. Ви точно в корені Git-проєкту?")
    sys.exit(1)

user_lang = input("Введіть мову для відповідей ШІ: ").strip()
if not user_lang:
    user_lang = "English"


bash_template = f"""#!/bin/bash
echo "🤖 Запуск AI Git-Hook Reviewer..."

export REVIEW_LANGUAGE="{user_lang}"

REPO_ROOT=$(git rev-parse --show-toplevel)

PYTHON_BIN="$REPO_ROOT/{venv_path.name}/bin/python"
MAIN_SCRIPT="$REPO_ROOT/main.py"

# Перевіряємо, чи існує venv, щоб видати нормальну помилку
if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ Помилка: Віртуальне середовище {venv_path.name} не знайдено у $REPO_ROOT"
    exit 1
fi

exec < /dev/tty

"$PYTHON_BIN" "$MAIN_SCRIPT"

RESULT=$?
exit $RESULT
"""

hook_file.write_text(bash_template, encoding="utf-8")
hook_file.chmod(0o755)
print("✅ Git Hook успішно встановлено у .git/hooks/pre-commit")