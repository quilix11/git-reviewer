import sys
from pathlib import Path

hooks_path = Path(".git/hooks")
hook_file = hooks_path / "pre-commit"
current_dir = Path(__file__).parent.absolute()
main_script_path = current_dir / "main.py"

if hooks_path.exists():
    print("✅ Папку hooks знайдено, продовжуємо...")
else:
    print("❌ Папку hooks не знайдено. Переконайтеся, що ви знаходитеся в корені git-репозиторію.")
    sys.exit(1)

bash_template = f"""#!/bin/bash
echo "🤖 Запуск AI Git-Hook Reviewer..."
REPO_ROOT=$(git rev-parse --show-toplevel)
PYTHON_CMD="$REPO_ROOT/.venv/bin/python"
MAIN_SCRIPT="{main_script_path}"

"$PYTHON_CMD" "$MAIN_SCRIPT"

RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "❌ Git Hook: Коміт скасовано!"
  exit 1
fi
exit 0
"""

hook_file.write_text(bash_template, encoding="utf-8")
hook_file.chmod(0o755)
print("✅ Git Hook успішно встановлено!")
