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

def main():

    my_diff = git_diff()

    if not my_diff:
        print("Немає змін для перевірки")
        sys.exit(0)

        # 3. Якщо зміни є - відправляємо ШІ та друкуємо звіт
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