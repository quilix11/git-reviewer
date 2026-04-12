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
from services.theme import console

load_dotenv()

def main():

    my_diff = git_diff()
    
    if not my_diff:
        console.print("[muted]No changes to review.[/muted]")
        sys.exit(0)

    with console.status("[info]AI is analyzing code...[/info]", spinner="dots"):
        ai_response = analyze_code(my_diff)
        clean_json = ai_response.strip().strip("`").removeprefix("json").strip()

        try:
            data = json.loads(clean_json)
            level = data.get("level", "INFO")
            report_text = data.get("report", "Error: Failed to get report from AI.")
        except json.JSONDecodeError as e:
            console.print(f"[error]Error parsing AI response: {e}[/error]")
            level = "CRITICAL"
            report_text = f"Failed to parse AI response as JSON. Possible format issue.\n\nOriginal response:\n```\n{ai_response}\n```"
        except KeyError as e:
            console.print(f"[error]AI response does not contain expected key: {e}[/error]")
            level = "CRITICAL"
            report_text = f"AI response has incorrect structure: missing key '{e}'.\n\nOriginal response:\n```\n{ai_response}\n```"

        if not isinstance(report_text, str):
            report_text = f"```json\n{json.dumps(report_text, ensure_ascii=False, indent=2)}\n```"   

    report_md = Markdown(report_text)
    console.print(Panel(
        report_md, 
        title="[info]AI CODE REVIEW[/info]", 
        border_style="panel_border"
    ))


    if level == "CRITICAL":
        console.print("[critical]Critical issues detected. Commit rejected.[/critical]")
        sys.exit(1)
    elif level == "WARNING":
        console.print("[warning]Potential issues detected. Recommended to fix before committing.[/warning]")
        try:
            if not Confirm.ask("Do you still want to commit these changes?"):
                console.print("[muted]Commit cancelled by user.[/muted]")
                sys.exit(1)
        except EOFError:
            console.print("[error]Input not available. Please run in an interactive terminal.[/error]")
            sys.exit(1)
    else:
        console.print("[success]Code looks good. Commit allowed.[/success]")

    


if __name__ == "__main__":
    main()
