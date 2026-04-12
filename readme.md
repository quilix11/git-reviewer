## Installation

### 1. Automatic Installation (Recommended)
Run this command in the root directory of your Git project to install the reviewer automatically:

```bash
curl -sSL https://raw.githubusercontent.com/quilix11/git-reviewer/main/install.sh | bash

```
This script will safely clone the repository, set up a virtual environment, install dependencies, and activate the pre-commit hook.
### 2. Manual Installation
If you prefer to set it up manually:
 1. Clone the repository into a hidden directory:
   ```bash
   git clone https://github.com/quilix11/git-reviewer.git
   
   ```
 2. Navigate to the directory:
   ```bash
   cd .git-reviewer
   
   ```
 3. Run the installer script with your preferred language as an argument:
   ```bash
   python install.py
   
   ```
   *Note: If no language is provided, it defaults to English.*
## Configuration
After installation, ensure you have a .env file inside the .git-reviewer folder with your credentials:
```env
API_KEY=your_google_gemini_api_key
AI_MODEL=(you Gemini model, example: gemini-2.5-fast

```
## How it Works
Once installed, the tool acts as a pre-commit hook. Every time you run git commit, the following happens:
 1. The script gathers your staged changes (git diff --staged).
 2. AI analyzes the code for security, logic, and quality issues.
 3. If **CRITICAL** issues are found, the commit is automatically blocked.
 4. If **WARNINGS** are found, you will be asked to confirm whether you want to proceed.

