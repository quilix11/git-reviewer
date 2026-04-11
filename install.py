import sys
from pathlib import Path

hooks_path = Path(".git/hooks")
hook_file = hooks_path / "pre-commit"

if not hooks_path.exists():
    print("❌ Папку .git/hooks не знайдено. Ви точно в корені Git-проєкту?")
    sys.exit(1)

bash_template = """#!/bin/bash
echo "🤖 Запуск AI Git-Hook Reviewer..."

# Git сам знає, де корінь репозиторію
REPO_ROOT=$(git rev-parse --show-toplevel)

# Використовуємо відносні шляхи від кореня
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
MAIN_SCRIPT="$REPO_ROOT/main.py"

# Перевіряємо, чи існує venv, щоб видати нормальну помилку
if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ Помилка: Віртуальне середовище .venv не знайдено у $REPO_ROOT"
    exit 1
fi

"$PYTHON_BIN" "$MAIN_SCRIPT"

RESULT=$?
exit $RESULT
"""

hook_file.write_text(bash_template, encoding="utf-8")
hook_file.chmod(0o755)
print("✅ Git Hook успішно встановлено у .git/hooks/pre-commit")