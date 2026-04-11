import sys
from services.ai_service import analyze_code
from services.git_utils import git_diff
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live

console = Console()


def main():

    my_diff = git_diff()

    if not my_diff:
        print("Немає змін для перевірки")
        sys.exit(0)

    print("ШІ аналізує код... Зачекайте...")
    ai_report = analyze_code(my_diff)
    print("\n--- ЗВІТ ШІ ---")
    print(ai_report)
    print("---------------\n")


    if "VERDICT: REJECT" in ai_report:
        print("❌ Коміт заблоковано через помилки або хардкод!")
        sys.exit(1)
    else:
        print("✅ Код перевірено, коміт дозволено!")
        sys.exit(0)


if __name__ == "__main__":
    main()