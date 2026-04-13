import os
import json
import sys
from dotenv import load_dotenv
from rich.panel import Panel
from services.ai_service import analyze_code
from services.git_utils import get_staged_diff
from services.theme import console

def main():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)

    my_diff = get_staged_diff()
    if not my_diff:
        return

    console.print("[info]Analyzing your changes...[/info]")
    
    try:
        ai_response = analyze_code(my_diff)
        
        clean_json = ai_response.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(clean_json)
            level = data.get("level", "INFO").upper()
            report = data.get("report", "No details provided.")
        except json.JSONDecodeError:
            level = "INFO"
            report = ai_response

        color = "red" if level == "CRITICAL" else "yellow" if level == "WARNING" else "green"
        
        console.print("\n")
        console.print(Panel(
            report,
            title=f"[bold {color}]AI Review: {level}[/bold {color}]",
            border_style=color,
            padding=(1, 2)
        ))

        if level == "CRITICAL":
            console.print(f"\n[bold red]❌ Commit blocked![/bold red] Fix critical issues and try again.")
            sys.exit(1)
        else:
            console.print(f"\n[bold green]✅ Code looks good![/bold green] Proceeding with commit...")
            sys.exit(0)
            
    except Exception as e:
        console.print(f"[error]AI Review skipped due to error: {e}[/error]")
        sys.exit(0)

if __name__ == "__main__":
    main()
