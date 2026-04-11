import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def analyze_code(diff_text):

    client = genai.Client(api_key=os.getenv("API_KEY"))

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
