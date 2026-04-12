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
        ai_report = analyze_code(my_diff)

    report_md = Markdown(ai_report)
    console.print(Panel(
        report_md, 
        title="[bold]AI CODE REVIEW[/bold]", 
        border_style="white"
    ))

    if "[CRITICAL]" in ai_report:
        console.print("[bold red]❌ Виявлено критичні проблеми. Коміт відхилено.[/bold red]")
        sys.exit(1)
    elif "[WARNING]" in ai_report:
        console.print("[bold yellow]⚠️ Виявлено потенційні проблеми. Рекомендується виправити перед комітом.[/bold yellow]")
        if not Confirm.ask("Ви все ще хочете комітити ці зміни?"):
            console.print("[bold red]Коміт скасовано користувачем.[/bold red]")
            sys.exit(1)
    else:
        console.print("[bold green]✅ Код виглядає добре. Коміт дозволено.[/bold green]")

    

if __name__ == "__main__":
    main()
