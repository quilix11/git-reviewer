import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv
from rich.prompt import Confirm
import json

from services.git_utils import git_diff
from services.ai_service import analyze_code

load_dotenv()

console = Console()

def main():

    my_diff = git_diff()
    
    if not my_diff:
        console.print("ℹ [bold]Немає змін для перевірки.[/bold]")
        sys.exit(0)

    with console.status("[bold white]ШІ аналізує код...[/bold white]", spinner="dots"):
        ai_response = analyze_code(my_diff)
        clean_json = ai_response.strip().strip("`").removeprefix("json").strip()

        try:
            data = json.loads(clean_json)
            level = data.get("level", "INFO")
            report_text = data.get("report", "Помилка: Не вдалося отримати звіт від ШІ.")
        except json.JSONDecodeError as e:
            console.print(f"[bold red]❌ Помилка при парсингу відповіді ШІ: {e}[/bold red]")
            level = "CRITICAL"
            report_text = f"[bold red]Не вдалося розібрати відповідь ШІ як JSON. Можлива проблема з форматом.[/bold red]\n\nОригінальна відповідь:\n```\n{ai_response}\n```"
        except KeyError as e:
            console.print(f"[bold red]❌ Відповідь ШІ не містить очікуваного ключа: {e}[/bold red]")
            level = "CRITICAL"
            report_text = f"[bold red]Відповідь ШІ має некоректну структуру: відсутній ключ '{e}'.[/bold red]\n\nОригінальна відповідь:\n```\n{ai_response}\n```"

        if not isinstance(report_text, str):
            report_text = f"```json\n{json.dumps(report_text, ensure_ascii=False, indent=2)}\n```"   

    report_md = Markdown(report_text)
    console.print(Panel(
        report_md, 
        title="[bold]AI CODE REVIEW[/bold]", 
        border_style="white"
    ))


    if level == "CRITICAL":
        console.print("[bold red]❌ Виявлено критичні проблеми. Коміт відхилено.[/bold red]")
        sys.exit(1)
    elif level == "WARNING":
        console.print("[bold yellow]⚠️ Виявлено потенційні проблеми. Рекомендується виправити перед комітом.[/bold yellow]")
        if not Confirm.ask("Ви все ще хочете комітити ці зміни?"):
            console.print("[bold red]Коміт скасовано користувачем.[/bold red]")
            sys.exit(1)
    else:
        console.print("[bold green]✅ Код виглядає добре. Коміт дозволено.[/bold green]")

    


if __name__ == "__main__":
    main()
