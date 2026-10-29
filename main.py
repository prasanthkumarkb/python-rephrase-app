import time

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    logger,
)

from cli_ui import (
    console,
    show_header,
    choose_style,
    get_input_text,
    show_result,
    show_error,
    show_goodbye,
)

from gemini_service import rephrase_text


def main():
    logger.info("Application started | model=%s", GEMINI_MODEL)

    if not GEMINI_API_KEY:
        show_error("GEMINI_API_KEY is missing in .env")
        return

    while True:
        try:
            show_header()

            console.print(f"[dim]AI Model: " f"{GEMINI_MODEL}[/dim]\n")

            style = choose_style()

            if style is None:
                show_goodbye()
                break

            text = get_input_text()

            if not text:
                show_error("Please enter some text.")
                console.input("\n[dim]Press Enter " "to continue...[/dim]")
                continue

            start_time = time.perf_counter()

            try:
                with console.status(
                    "[bold yellow]" "Rephrasing your text..." "[/bold yellow]",
                    spinner="dots",
                ):
                    result = rephrase_text(text, style)

                elapsed = time.perf_counter() - start_time

                logger.info(
                    "Request completed | " "style=%s | time=%.2fs",
                    style,
                    elapsed,
                )

                show_result(
                    result,
                    style,
                    elapsed,
                )

            except Exception as exc:
                logger.error("Request error: %s", exc)

                show_error("Unable to rephrase the text.\n" f"Details: {exc}")

            console.input("\n[dim]Press Enter " "to return to menu...[/dim]")

        except (KeyboardInterrupt, EOFError):
            console.print()
            show_goodbye()
            break

    logger.info("Application stopped")


if __name__ == "__main__":
    main()
