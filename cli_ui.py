from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

WRITING_STYLES = {
    "1": {
        "key": "professional",
        "name": "Professional",
        "description": "Business-ready writing",
    },
    "2": {
        "key": "polite",
        "name": "Polite",
        "description": "Friendly and respectful",
    },
    "3": {
        "key": "simple",
        "name": "Simple",
        "description": "Clear and concise",
    },
    "4": {
        "key": "formal",
        "name": "Formal",
        "description": "Official communication",
    },
}


def show_header():
    console.clear()

    console.print(
        Panel(
            "[bold bright_cyan]AI REPHRASE[/bold bright_cyan]\n"
            "[dim]Your AI-powered writing assistant[/dim]",
            border_style="bright_cyan",
            padding=(1, 3),
            expand=True,
        )
    )


def choose_style():
    table = Table(
        title="[bold cyan]Choose Writing Style[/bold cyan]",
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold cyan",
        expand=True,
    )

    table.add_column("Option", style="bold yellow", width=8)

    table.add_column("Style", style="bold white")

    table.add_column("Description", style="dim")

    for number, style in WRITING_STYLES.items():
        table.add_row(
            number,
            style["name"],
            style["description"],
        )

    table.add_row("0", "Exit", "Close the application")

    console.print(table)

    choice = Prompt.ask(
        "\n[bold yellow]Enter choice[/bold yellow]",
        choices=["0", "1", "2", "3", "4"],
        show_choices=False,
    )

    if choice == "0":
        return None

    return WRITING_STYLES[choice]["key"]


def get_input_text():
    console.print("\n[bold bright_cyan]" "Enter text to rephrase" "[/bold bright_cyan]")

    console.print("[dim]Press Enter to submit your text.[/dim]")

    return Prompt.ask("[bold green]Text[/bold green]").strip()


def show_result(text, style, elapsed):
    console.print()

    console.print(
        Panel(
            text,
            title=("[bold green]" "Rephrased Successfully" "[/bold green]"),
            subtitle=(f"[dim]Style: {style.title()} " f"| Time: {elapsed:.2f}s[/dim]"),
            border_style="green",
            padding=(1, 2),
            expand=True,
        )
    )


def show_error(message):
    console.print(
        Panel(
            str(message),
            title="[bold red]Error[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
    )


def show_goodbye():
    console.print("\n[bold green]" "Thank you for using AI Rephrase!" "[/bold green]")
