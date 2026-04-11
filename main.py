import os
import sys
import subprocess as sp
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("API_KEY")



def git_diff():
    process = sp.run(["git", "diff","--staged"], capture_output=True, text=True, encoding="utf-8")
    return process.stdout


def analyze_code(diff_text):

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model=os.getenv("AI_MODEL"),
        contents=(f"Ти - суворий Senior розробник."
                  f"але пиши коротко та чітко не потрібно показувати щось з себе тільки факти та як щось виправити"
                  f" Перевір цей git diff і скажи,"
                  f" чи є тут хардкод або помилки:\n{diff_text}"
                  f"В кінці свого звіту ти зобов'язаний"
                  f" написати з нового рядка одне з двох: 'VERDICT: REJECT' "
                  f"(якщо є хардкод або критичні помилки) або 'VERDICT: ACCEPT' (якщо код нормальний).")
    )
    return response.text

my_diff = git_diff()

if not my_diff:
    print("Немає змін для перевірки")
else:
    diff = analyze_code(my_diff)
    print(diff)

if "VERDICT: REJECT" in diff:
    print("Коміт відхилено")
    sys.exit(1)
else:
    print("Код перевірений, комітимо")
    sys.exit(0)