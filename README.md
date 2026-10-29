# AI Text Rephrasing Tool

A simple Python command-line application that uses **Google Gemini AI** to rephrase text in different writing styles.

The application helps improve grammar, clarity, and sentence structure while preserving the original meaning.

## Features

- AI-powered text rephrasing using Google Gemini
- Four writing styles: Professional, Polite, Simple, and Formal
- Animated loading spinner during API requests
- API response-time tracking
- Application logging and error handling
- Environment-based API key configuration
- Supports Google Gemini's free API tier, subject to usage limits

## Technologies Used

- Python 3.10+
- Google Gemini API
- `google-genai`
- `python-dotenv`
- Python `logging` and `threading`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/python-rephrase-app.git
cd python-rephrase-app
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install google-genai python-dotenv
```

Or, if a `requirements.txt` file is included:

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Generate a free-tier API key using [Google AI Studio](https://aistudio.google.com/api-keys).

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

Choose a Gemini model available to your API account.

**Security:** Never commit your `.env` file or API key to GitHub.

### 5. Run the application

```bash
python main.py
```

## Usage

When the application starts, choose your preferred writing style:

```text
=== AI Text Rephrasing Tool ===

Choose writing style:
1. Professional
2. Polite
3. Simple
4. Formal
0. Exit

Enter choice: 2

Enter text to rephrase:
parking water leakage still there any update?
```

Example output:

```text
Rephrasing your text...

--- Rephrased Text ---

The water leakage issue in the parking area
still persists. Could you please provide
an update on its resolution?
```

## Writing Styles

| Style        | Description                          |
| ------------ | ------------------------------------ |
| Professional | Suitable for workplace communication |
| Polite       | Suitable for requests and messages   |
| Simple       | Clear and easy-to-understand English |
| Formal       | Suitable for official communication  |

## Logging

The application records API requests, execution times, successful responses, and errors.

Logs are stored in:

```text
logs/app.log
```

Example:

```text
2026-10-29 06:20:10 | INFO | Application started
2026-10-29 06:20:15 | INFO | Rephrase request started | style=polite | chars=45
2026-10-29 06:20:17 | INFO | Rephrase successful | time=2.13s | output_chars=108
```

Sensitive input text and API keys should not be recorded in logs.

## Project Structure

```text
python-rephrase-app/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── logs/
    └── app.log
```

The `logs` directory is automatically created when the application runs.

## Git Ignore

Ensure your `.gitignore` contains:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
logs/
```

## Troubleshooting

**ImportError: cannot import name 'genai' from 'google'**

Install the correct package:

```bash
python -m pip install --upgrade google-genai
```

**404 NOT_FOUND: Model not found**

Check that the configured Gemini model exists and supports `generateContent` for your account.

**API requests are slow**

Try a lightweight model such as `gemini-2.5-flash-lite`, if available, and check the response times recorded in `logs/app.log`.

**API key missing**

Verify that `.env` contains a valid `GEMINI_API_KEY`.

## Future Enhancements

- Web interface using Streamlit
- REST API using FastAPI
- Text history and clipboard integration
- Additional writing styles
- Batch text rephrasing

## License

No license has been specified yet. Add a `LICENSE` file if you want to grant others permission to use, modify, or distribute the project.

## Author

Developed as a Python learning project using Google Gemini AI.
