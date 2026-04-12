import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def analyze_code(diff_text):

    client = genai.Client(api_key=os.getenv("API_KEY"))

    response = client.models.generate_content(
        model=os.getenv("AI_MODEL"),
        contents=(f"Ти суворий автоматичний Code Reviewer."
                  f"Твоя мета - перевірити git diff." 
                  f"Пиши максимально коротко: 'Проблема: ... -> Рішення: ...'." 
                  f"Жодної води, вітань чи загальних висновків."
                  f"Кожен знайдений пункт ти ЗОБОВ'ЯЗАНИЙ починати з тегу'"
                  f"[INFO] - це для порад/інформації, "
                  f"[WARNING] - для некритичних помилок/поганих практик,"
                  f"[CRITICAL] - для хардкоду, синтаксичних помилок, вразливостей,"
                  f"залежно від рівня загрози. Ось diff: {diff_text}")
    )
    return response.text
