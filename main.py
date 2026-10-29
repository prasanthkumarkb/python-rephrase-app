import os
import sys
import time
import logging
import threading
from pathlib import Path
from itertools import cycle

from dotenv import load_dotenv
from google import genai

# ----------------------------------
# 1. Environment Configuration
# ----------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=API_KEY)


# ----------------------------------
# 2. Logging Configuration
# ----------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s | %(levelname)s | " "%(message)s"),
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("RephraseApp")


# ----------------------------------
# 3. Loading Spinner
# ----------------------------------


def show_loader(stop_event):
    spinner = cycle(["|", "/", "-", "\\"])

    while not stop_event.is_set():
        symbol = next(spinner)

        print(f"\r{symbol} Rephrasing your text...", end="", flush=True)

        stop_event.wait(0.1)

    print("\r" + " " * 45 + "\r", end="", flush=True)


# ----------------------------------
# 4. Gemini Rephrase Function
# ----------------------------------


def rephrase_text(text, style="polite"):

    logger.info("Rephrase request started | style=%s | chars=%d", style, len(text))

    prompt = f"""
    You are an English writing assistant.

    Rephrase the following text in a {style} tone.

    Rules:
    - Correct grammar and spelling.
    - Preserve the original meaning.
    - Make the sentence clear and natural.
    - Do not add new information.
    - Return only the rephrased text.

    Text:
    {text}
    """

    start_time = time.perf_counter()

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"), contents=prompt
        )

        result = response.text

        if not result:
            raise ValueError("Empty response from Gemini")

        elapsed = time.perf_counter() - start_time

        logger.info(
            "Rephrase successful | time=%.2fs | output_chars=%d", elapsed, len(result)
        )

        return result.strip()

    except Exception:
        elapsed = time.perf_counter() - start_time

        logger.exception("Rephrase failed | time=%.2fs", elapsed)

        raise


# ----------------------------------
# 5. Main Application
# ----------------------------------


def main():

    styles = {"1": "professional", "2": "polite", "3": "simple", "4": "formal"}

    print("\n=== AI Text Rephrasing Tool ===")

    logger.info("Application started")

    while True:

        print("\nChoose writing style:")
        print("1. Professional")
        print("2. Polite")
        print("3. Simple")
        print("4. Formal")
        print("0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            logger.info("Application closed")
            print("Goodbye!")
            break

        if choice not in styles:
            print("Invalid choice")
            continue

        text = input("\nEnter text to rephrase:\n").strip()

        if not text:
            print("Text cannot be empty")
            continue

        stop_event = threading.Event()

        loader_thread = threading.Thread(
            target=show_loader, args=(stop_event,), daemon=True
        )

        try:
            loader_thread.start()

            result = rephrase_text(text, styles[choice])

            print("\n--- Rephrased Text ---")
            print(result)
            print("-----------------------")

        except Exception as error:
            print(f"\nError: {error}")

        finally:
            stop_event.set()
            loader_thread.join()


if __name__ == "__main__":
    main()
