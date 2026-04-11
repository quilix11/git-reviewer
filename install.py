import sys
from pathlib import Path

hooks_path = Path(".git/hooks")
hook_file = hooks_path / "pre-commit"

if hooks_path.exists():
    print("✅ Папку hooks знайдено, продовжуємо...")
else:
    print("❌ Папку hooks не знайдено. Переконайтеся, що ви знаходитеся в корені git-репозиторію.")
    sys.exit(1)

bash_script ="""#!/bin/bash
echo "🤖 Запуск AI Git-Hook Reviewer..."
./.venv/bin/python main.py
RESULT=$?
if [ $RESULT -ne 0 ]; then
echo "❌ Git Hook: Коміт скасовано!"
exit 1
fi
exit 0"""

hook_file.write_text(bash_script, encoding="utf-8")
hook_file.chmod(0o755)

