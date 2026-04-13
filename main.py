import os
from dotenv import load_dotenv
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
        console.print("\n[bold blue]AI Code Review:[/bold blue]")
        console.print(ai_response)
        
        if "CRITICAL" in ai_response.upper() or "SECURITY" in ai_response.upper():
            console.print("\n[error]Commit blocked due to critical issues.[/error]")
            exit(1)
            
    except Exception as e:
        console.print(f"[error]Error: {e}[/error]")
        exit(0)

if __name__ == "__main__":
    main()