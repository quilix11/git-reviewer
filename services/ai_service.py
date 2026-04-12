import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def analyze_code(diff_text):
    language = os.getenv("REVIEW_LANGUAGE", "English")

    client = genai.Client(api_key=os.getenv("API_KEY"))

    response = client.models.generate_content(
        model=os.getenv("AI_MODEL"),
        contents=f"""You are a strict and highly experienced Senior/Staff Code Reviewer.

You MUST respond in the following language: {language}

Your task is to analyze the provided git diff and produce a precise, critical, and actionable review.

You must evaluate the code using language-agnostic best practices and engineering standards.

Evaluation criteria:

1. Security:
- hardcoded secrets (API keys, tokens, passwords)
- injection vulnerabilities (SQL, command, XSS, etc.)
- unsafe input/output handling
- missing validation or sanitization

2. Logic and correctness:
- potential bugs
- incorrect conditions or edge cases
- race conditions or concurrency issues
- improper error handling

3. Code quality:
- DRY violations (duplication)
- KISS violations (unnecessary complexity)
- SRP violations (too many responsibilities)
- magic numbers or strings
- deep nesting
- unclear or misleading naming

4. Style and consistency:
- inconsistent naming conventions
- mixed styles (camelCase, snake_case, etc.)
- poor readability
- overly large functions
- unnecessary or missing comments
- formatting inconsistencies

5. Testability:
- tight coupling
- low modularity
- hard-to-test logic
- missing validation paths

6. Performance:
- unnecessary computations
- inefficient algorithms
- memory misuse
- blocking operations where avoidable

Rules:
- Focus only on the changes in the diff
- Do not invent issues if none exist
- Be strict but accurate
- Avoid generic statements
- Provide specific and actionable feedback
- DO NOT use any emojis in the report

Classification:
- CRITICAL: security issues or serious bugs
- WARNING: bad practices or risky patterns
- INFO: minor improvements or clean code

Response format (STRICTLY REQUIRED):
Return ONLY valid JSON. No extra text.

{{
  "level": "CRITICAL | WARNING | INFO",
  "report": "Detailed report with structured sections. For each issue include: what is wrong, why it is a problem, and how to fix it with an example if possible."
}}

Git diff:
{diff_text}
"""
    )
    return response.text
