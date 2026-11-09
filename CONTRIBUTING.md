# Contributing to Poll Results Visualizer

Thank you for your interest in contributing to the **Poll Results Visualizer** project, maintained by **Akash Das**.

## Development Workflow

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd poll-results-visualizer
   ```

2. **Set up the virtual environment**:
   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows Command Prompt:
     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```
   - macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run the test suite**:
   ```bash
   pytest
   ```

5. **Run the application**:
   ```bash
   python -m streamlit run app/streamlit_app.py
   ```
   or:
   ```bash
   python run.py
   ```

## Code Guidelines
- Keep core logic inside `src/` modules; keep UI presentation in `app/`.
- Ensure new features have accompanying unit tests in `tests/`.
- Maintain standard column naming: `respondent_id`, `question`, `option`, `response_date`, `segment`.
- Adhere to PEP 8 standards.

## Authorship
Project Author: **Akash Das**
